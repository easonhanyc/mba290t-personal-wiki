"""The retrieval tool: passages in, ranked evidence out. No language model is involved.

Index build:  raw sources + reviewed wiki notes -> passages (data/chunks.jsonl)
              -> EmbeddingGemma vectors (data/vectors.npy), reused when a passage's text is unchanged.
Search:       BM25 over passage words  +  cosine over vectors  ->  reciprocal-rank fusion.
              If the embedding server is not running, search degrades to BM25 alone and says so.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from . import config
from .embed import Embedder, doc_text
from .textparse import SUPPORTED, Document, Section, parse_file


@dataclass
class Chunk:
    id: str
    kind: str          # "source" (original evidence) or "wiki" (reviewed note)
    path: str          # vault-relative, e.g. raw/course/syllabus.html
    title: str
    section: str
    line_start: int
    line_end: int
    text: str

    @property
    def hash(self) -> str:
        return hashlib.sha256(f"{self.title}|{self.section}|{self.text}".encode()).hexdigest()[:16]

    @property
    def location(self) -> str:
        return f"{self.path}:{self.line_start}-{self.line_end}"


@dataclass
class Hit:
    chunk: Chunk
    score: float
    bm25_rank: int | None
    vector_rank: int | None
    bm25_score: float = 0.0
    cosine: float | None = None


# --------------------------------------------------------------------------- chunking

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“(*])")


MAX_CHARS = 1500  # dense tables tokenize at ~1 token per 2-3 characters; keep passages well under 1K tokens


def _too_big(text: str, max_words: int) -> bool:
    return len(text.split()) > max_words or len(text) > MAX_CHARS


def _split_long(text: str, max_words: int) -> list[str]:
    """Split an oversized block: by lines first (tables, lists), then by sentences."""
    if not _too_big(text, max_words):
        return [text]
    units = text.split("\n") if "\n" in text else _SENT.split(text)
    if len(units) == 1:
        units = _SENT.split(text)
    parts, cur = [], []
    sep = "\n" if "\n" in text else " "
    for unit in units:
        if cur and _too_big(sep.join(cur + [unit]), max_words):
            parts.append(sep.join(cur))
            cur = []
        cur.append(unit)
    if cur:
        parts.append(sep.join(cur))
    # A single sentence or row can still be too long; hard-wrap it by characters as a last resort.
    out = []
    for part in parts:
        while len(part) > MAX_CHARS:
            cut = part.rfind(" ", 0, MAX_CHARS)
            cut = cut if cut > MAX_CHARS // 2 else MAX_CHARS
            out.append(part[:cut])
            part = part[cut:].lstrip()
        out.append(part)
    return out


def chunk_section(section: Section, target: int, max_words: int):
    """Yield (line_start, line_end, text) passages; a passage never spans two sections."""
    buf: list[str] = []
    start = end = 0
    for block in section.blocks:
        cursor = 0
        for piece in _split_long(block.text, max_words):
            # Line of this piece inside the block: exact for lists and tables (one source line per text line).
            pos = block.text.find(piece[:60], cursor)
            pos = pos if pos >= 0 else cursor
            cursor = pos + len(piece)
            p_start = min(block.line + block.text.count("\n", 0, pos), block.end_line)
            p_end = min(p_start + piece.count("\n"), block.end_line) if piece != block.text else block.end_line
            joined = "\n".join(buf + [piece])
            if buf and (len(joined.split()) > target or len(joined) > MAX_CHARS):
                yield start, end, "\n".join(buf)
                buf = []
            if not buf:
                start = p_start
            buf.append(piece)
            end = max(p_end, start)
    if buf:
        yield start, end, "\n".join(buf)


def chunk_document(doc: Document, kind: str, rel_path: str, target: int, max_words: int) -> list[Chunk]:
    chunks = []
    for section in doc.sections:
        if kind == "wiki" and section.kind == "properties":
            continue  # note metadata (ids, hashes) is for the machine, not evidence
        for i, (a, b, text) in enumerate(chunk_section(section, target, max_words)):
            cid = f"{rel_path}#L{a}-{b}.{i}"
            chunks.append(Chunk(id=cid, kind=kind, path=rel_path, title=doc.title, section=section.label,
                                line_start=a, line_end=b, text=text))
    return chunks


# --------------------------------------------------------------------------- BM25

_STOP = set("""a an and are as at be been but by can did do does for from had has have how i if in into is it its
me my of on or our so than that the their them then there these they this to was we were what when where which who
why will with you your""".split())
_TOKEN = re.compile(r"[a-z0-9]+(?:[.'][a-z0-9]+)*%?")


def _stem(tok: str) -> str:
    for suf in ("ing", "edly", "ed", "es", "s"):
        if len(tok) > len(suf) + 3 and tok.endswith(suf) and not tok[-len(suf) - 1].isdigit():
            return tok[: -len(suf)]
    return tok


def tokenize(text: str) -> list[str]:
    toks = (t[:-2] if t.endswith("'s") else t for t in _TOKEN.findall(text.lower()))
    return [_stem(t) for t in toks if t not in _STOP]


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tfs = [Counter(d) for d in docs]
        self.lens = [len(d) for d in docs]
        self.avg = sum(self.lens) / max(1, len(docs))
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(len(self.tfs), dtype=np.float32)
        for t in set(query):
            idf = self.idf.get(t)
            if idf is None:
                continue
            for i, tf in enumerate(self.tfs):
                f = tf.get(t)
                if f:
                    denom = f + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg)
                    out[i] += idf * f * (self.k1 + 1) / denom
        return out


# --------------------------------------------------------------------------- index files

def _data(settings: config.Settings) -> Path:
    d = settings.path("data")
    d.mkdir(parents=True, exist_ok=True)
    return d


def is_reviewed_note(path: Path) -> bool:
    head = path.read_text(encoding="utf-8", errors="replace")[:2000]
    return bool(re.search(r"^reviewed:\s*true\s*$", head, re.M))


def collect_documents(settings: config.Settings) -> list[tuple[str, Path]]:
    """(kind, path) for every file the index should contain."""
    vault = settings.vault
    items = []
    for p in sorted(settings.path("raw").rglob("*")):
        if p.is_file() and p.suffix.lower() in SUPPORTED and not p.name.startswith("."):
            items.append(("source", p))
    for p in sorted(settings.path("wiki").rglob("*.md")):
        if is_reviewed_note(p):
            items.append(("wiki", p))
    return [(k, p) for k, p in items if vault in p.parents]


def build_index(settings: config.Settings | None = None, embedder: Embedder | None = None, log=print) -> dict:
    settings = settings or config.load()
    r = settings.retrieval
    vault = settings.vault
    chunks: list[Chunk] = []
    for kind, path in collect_documents(settings):
        doc = parse_file(path)
        chunks.extend(chunk_document(doc, kind, path.relative_to(vault).as_posix(), r["target_words"], r["max_words"]))

    data = _data(settings)
    with open(data / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")

    # Reuse vectors for passages whose text is unchanged; embed only the new ones.
    old = {}
    if (data / "vectors.npy").exists() and (data / "vectors_meta.json").exists():
        meta = json.loads((data / "vectors_meta.json").read_text())
        vecs = np.load(data / "vectors.npy")
        if meta.get("model") == settings.local["embed_model_id"] and len(meta.get("hashes", [])) == len(vecs):
            old = {h: vecs[i] for i, h in enumerate(meta["hashes"])}
    embedder = embedder or Embedder(settings)
    hashes = [c.hash for c in chunks]
    todo = [i for i, h in enumerate(hashes) if h not in old]
    stats = {"passages": len(chunks), "sources": len({c.path for c in chunks if c.kind == "source"}),
             "wiki_notes": len({c.path for c in chunks if c.kind == "wiki"}), "embedded_new": 0,
             "reused_vectors": len(chunks) - len(todo), "vectors": False}
    if todo and not embedder.available():
        log("  ! Embedding server not running: vector index not updated (search will use BM25 only). "
            "Start it with `wiki serve start` and re-run `wiki ingest`.")
        (data / "vectors_meta.json").unlink(missing_ok=True)
        return stats
    new = embedder.embed([doc_text(f"{chunks[i].title} › {chunks[i].section}", chunks[i].text) for i in todo]) if todo else None
    dim = new.shape[1] if new is not None else (len(next(iter(old.values()))) if old else 768)
    mat = np.zeros((len(chunks), dim), dtype=np.float32)
    j = 0
    for i, h in enumerate(hashes):
        if h in old:
            mat[i] = old[h]
        else:
            mat[i] = new[j]
            j += 1
    np.save(data / "vectors.npy", mat)
    (data / "vectors_meta.json").write_text(json.dumps({"model": settings.local["embed_model_id"], "hashes": hashes}))
    stats.update(embedded_new=len(todo), vectors=True)
    return stats


# --------------------------------------------------------------------------- search

class Index:
    def __init__(self, settings: config.Settings | None = None):
        self.settings = settings or config.load()
        data = _data(self.settings)
        path = data / "chunks.jsonl"
        if not path.exists():
            raise FileNotFoundError("The retrieval index is empty. Run `wiki ingest` first.")
        self.chunks = [Chunk(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line]
        r = self.settings.retrieval
        self.bm25 = BM25([tokenize(f"{c.title} {c.section} {c.text}") for c in self.chunks], r["bm25_k1"], r["bm25_b"])
        self.vectors = None
        meta_path = data / "vectors_meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            if meta.get("hashes") == [c.hash for c in self.chunks]:
                self.vectors = np.load(data / "vectors.npy")
        self.embedder = Embedder(self.settings)
        self.last_method = ""

    def search(self, query: str, k: int | None = None, kinds: tuple[str, ...] = ("source", "wiki"),
               use: str = "hybrid") -> list[Hit]:
        """use="hybrid" (default), or "bm25" / "vector" alone (for the retrieval ablation)."""
        r = self.settings.retrieval
        k = k or r["top_k"]
        allowed = np.array([c.kind in kinds for c in self.chunks])
        bm = self.bm25.scores(tokenize(query))
        bm_order = [i for i in np.argsort(-bm) if bm[i] > 0 and allowed[i]][: r["candidates"]] if use != "vector" else []

        vec_order: list[int] = []
        cos = None
        if use != "bm25" and self.vectors is not None and self.embedder.available():
            q = self.embedder.embed_query(query)
            cos = self.vectors @ q
            vec_order = [i for i in np.argsort(-cos) if allowed[i]][: r["candidates"]]
            self.last_method = "hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion)" if use == "hybrid" else "EmbeddingGemma vectors only"
        else:
            reason = "ablation" if use == "bm25" else "embedding server not running" if self.vectors is not None else "no vector index"
            self.last_method = f"BM25 only ({reason})"

        fused: dict[int, float] = {}
        for rank, i in enumerate(bm_order, 1):
            fused[i] = fused.get(i, 0.0) + 1.0 / (r["rrf_k"] + rank)
        for rank, i in enumerate(vec_order, 1):
            fused[i] = fused.get(i, 0.0) + 1.0 / (r["rrf_k"] + rank)
        bm_rank = {i: n for n, i in enumerate(bm_order, 1)}
        vec_rank = {i: n for n, i in enumerate(vec_order, 1)}
        best = sorted(fused, key=lambda i: -fused[i])[:k]
        return [Hit(chunk=self.chunks[i], score=fused[i], bm25_rank=bm_rank.get(i), vector_rank=vec_rank.get(i),
                    bm25_score=float(bm[i]), cosine=None if cos is None else float(cos[i])) for i in best]
