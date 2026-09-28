"""The Obsidian vault: note files, naming rules, links, lint, rename, index and source catalog.

Machine identifiers (source ids, sha256, original file names) live in note properties and in
data/catalog.json. File names, headings and graph labels are the human subject names.
"""

from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import yaml

from . import config
from .textparse import parse_file

FOLDERS = ["Projects", "Experience", "Course", "Concepts"]
FOLDER_BLURB = {
    "Projects": "Things built, analysed or shipped — course assignments and portfolio work.",
    "Experience": "Employers, roles and schools.",
    "Course": "MBA 290T: schedule, assignments and policies.",
    "Concepts": "Techniques and ideas that show up across several projects.",
}


# --------------------------------------------------------------------------- note files

@dataclass
class Note:
    path: Path
    meta: dict = field(default_factory=dict)
    body: str = ""

    @property
    def title(self) -> str:
        return self.path.stem

    @property
    def folder(self) -> str:
        return self.path.parent.name

    def rel(self, vault: Path) -> str:
        return self.path.relative_to(vault).as_posix()

    @property
    def h1(self) -> str | None:
        m = re.search(r"^# (.+)$", self.body, re.M)
        return m.group(1).strip() if m else None


def read_note(path: Path) -> Note:
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            meta = yaml.safe_load(text[4:end]) or {}
            body = text[end + 5:]
    return Note(path=path, meta=meta, body=body.lstrip("\n"))


def write_note(note: Note) -> None:
    note.path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(note.meta, sort_keys=False, allow_unicode=True, width=1000).strip()
    note.path.write_text(f"---\n{front}\n---\n\n{note.body.strip()}\n", encoding="utf-8")


def all_notes(settings: config.Settings | None = None) -> list[Note]:
    settings = settings or config.load()
    return [read_note(p) for p in sorted(settings.path("wiki").rglob("*.md"))]


# --------------------------------------------------------------------------- naming

_SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}
_BAD_CHARS = re.compile(r'[\[\]#^|\\/:*?"<>]')
_GENERIC_TAIL = {"experience", "project", "overview", "summary", "notes", "note", "page", "details", "role", "position", "job", "implementation", "study"}
_BANNED = {"task", "chunk", "export", "untitled", "copy", "draft", "readme", "notes", "note", "part"}


def clean_title(raw: str) -> str:
    t = re.sub(r"\s+", " ", str(raw)).strip().strip("\"'")
    # Drop subtitles: "Action Hub — Ranked Alerts" -> "Action Hub"
    for sep in (" — ", " – ", " - ", ": "):
        if sep in t and len(t.split(sep)[0].split()) >= 1:
            head = t.split(sep)[0].strip()
            if head and len(t.split()) > 4:
                t = head
                break
    t = _BAD_CHARS.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip(" .,;-–—")
    # Name the subject, not the kind of page: "Amazon Web Services Experience" -> "Amazon Web Services".
    parts = t.split(" ")
    while len(parts) > 1 and parts[-1].lower() in _GENERIC_TAIL:
        parts.pop()
    t = " ".join(parts)
    if t.endswith("Ms"):
        t += "."
    words = t.split(" ")
    out = []
    for i, w in enumerate(words):
        if w.islower() and not re.search(r"\d", w):
            w = w if (i > 0 and w in _SMALL) else w[:1].upper() + w[1:]
        out.append(w)
    return " ".join(out)


def naming_problems(title: str) -> list[str]:
    problems = []
    words = title.split()
    if not words:
        return ["empty title"]
    if len(words) > 6:
        problems.append(f"{len(words)} words (keep 2–6)")
    if re.search(r"\b(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{6,}\b", title.lower()):
        problems.append("looks like a hash or ID")
    if re.search(r"\d{4}-\d{2}-\d{2}|\d{8,}|\d{1,2}:\d{2}", title):
        problems.append("contains a date or timestamp")
    if {w.lower().strip(".,") for w in words} & _BANNED:
        problems.append("contains a machine/export word (task, chunk, export, readme, ...)")
    if title.rstrip().endswith(("?", "!")) or re.search(r"\b(is|are|was|were|how|why|what)\b", title.lower()):
        problems.append("reads like a sentence or question")
    if _BAD_CHARS.search(title):
        problems.append("contains characters that break Obsidian links")
    if "_" in title or re.search(r"\w-\w+-\w+-", title):
        problems.append("looks like a slug, not a subject name")
    return problems


def norm(title: str) -> str:
    t = re.sub(r"[^a-z0-9 ]+", " ", title.lower())
    return " ".join(w for w in t.split() if w not in {"the", "a", "an"})


def similar(a: str, b: str) -> bool:
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    ta, tb = set(na.split()), set(nb.split())
    jaccard = len(ta & tb) / len(ta | tb)
    if jaccard >= 0.75 or difflib.SequenceMatcher(None, na, nb).ratio() >= 0.9:
        return True
    # "Pac-Man DQN Methodology Study" and "Ms. Pac-Man DQN Implementation" name the same subject once
    # words that describe the kind of write-up are ignored: compare the distinctive cores.
    ca, cb = ta - _DESCRIPTIVE, tb - _DESCRIPTIVE
    return len(ca & cb) >= 2 and (ca <= cb or cb <= ca)


_DESCRIPTIVE = {"implementation", "study", "methodology", "project", "app", "application", "agent", "experiments",
                "experiment", "system", "analysis", "overview", "report", "writeup", "documentation", "docs", "guide",
                "how", "works", "it", "details", "architecture", "design", "case", "ms", "mr", "training", "build",
                "building", "results", "summary", "notes", "note", "course", "program", "programme"}


_ABBREV = {"ms", "mr", "mrs", "dr", "st", "vs", "e.g", "i.e", "inc", "no", "u.s", "b.b.a", "b.s", "m.eng", "etc"}


def first_sentence(text: str) -> str:
    """First sentence of a summary, without splitting on "Ms." or "M.Eng." (used for index descriptions)."""
    text = re.sub(r"\s+", " ", text or "").strip()
    for m in re.finditer(r"[.!?](?=\s+[A-Z\"“(])", text):
        word = re.search(r"([\w.]+)$", text[:m.start()])
        token = word.group(1).lower() if word else ""
        if token in _ABBREV or len(token) == 1 or "." in token:
            continue
        return text[:m.end()]
    return text


# --------------------------------------------------------------------------- links

LINK = re.compile(r"(!?)\[\[([^\]|#]*)(#[^\]|]*)?(\|[^\]]*)?\]\]")


def _file_index(vault: Path) -> dict[str, list[Path]]:
    """Obsidian-style lookup keys -> files. Keys: vault path with/without .md, and bare name."""
    idx: dict[str, list[Path]] = {}
    for p in vault.rglob("*"):
        if not p.is_file() or ".obsidian" in p.parts:
            continue
        rel = p.relative_to(vault).as_posix()
        keys = {rel.lower()}
        if p.suffix == ".md":
            keys |= {rel[:-3].lower(), p.stem.lower()}
        else:
            keys.add(p.name.lower())
        for k in keys:
            idx.setdefault(k, []).append(p)
    return idx


def resolve(target: str, index: dict[str, list[Path]]) -> list[Path]:
    key = target.strip().lower()
    return sorted(set(index.get(key, [])))


def heading_ok(path: Path, anchor: str) -> bool:
    if path.suffix.lower() != ".md":
        return True  # Obsidian cannot jump inside HTML files; the file link alone is used
    heading = anchor.lstrip("#").strip().lower()
    doc = parse_file(path)
    return any(h.lower() == heading for h in doc.headings()) or heading == doc.title.lower()


def raw_link(rel_raw: str, heading: str | None, label: str) -> str:
    """Link from a note to an original source, jumping to the section when Obsidian can."""
    target = rel_raw[:-3] if rel_raw.endswith(".md") else rel_raw
    anchor = ""
    if heading and rel_raw.endswith(".md") and re.fullmatch(r"[\w\s,.'’()&—–%+-]+", heading):
        anchor = f"#{heading}"
    return f"[[{target}{anchor}|{label}]]"


# --------------------------------------------------------------------------- lint

def lint(settings: config.Settings | None = None) -> dict:
    settings = settings or config.load()
    vault = settings.vault
    index = _file_index(vault)
    notes = all_notes(settings)
    errors: list[str] = []
    warnings: list[str] = []
    index_text = (vault / "index.md").read_text(encoding="utf-8") if (vault / "index.md").exists() else ""
    index_links = {m.group(2).strip().rstrip("\\").lower() for m in LINK.finditer(index_text)}
    seen: dict[str, str] = {}
    link_count = broken = 0
    inbound: dict[str, int] = {n.title.lower(): 0 for n in notes}

    md_files = [vault / "index.md", vault / "Source Catalog.md", *[n.path for n in notes]]
    for path in md_files:
        if not path.exists():
            errors.append(f"missing {path.relative_to(vault)}")
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(vault).as_posix()
        for m in LINK.finditer(text):
            link_count += 1
            target, anchor = m.group(2).rstrip("\\"), m.group(3)  # "\|" is an escaped alias inside tables
            hits = resolve(target, index)
            if not hits:
                broken += 1
                errors.append(f"{rel}: broken link [[{target}]]")
            elif len(hits) > 1:
                broken += 1
                errors.append(f"{rel}: ambiguous link [[{target}]] -> {len(hits)} files")
            else:
                if anchor and not heading_ok(hits[0], anchor):
                    errors.append(f"{rel}: heading {anchor} not found in {hits[0].relative_to(vault)}")
                if path.parent != vault and hits[0].stem.lower() in inbound and hits[0] != path:
                    inbound[hits[0].stem.lower()] += 1

    for n in notes:
        rel = n.rel(vault)
        if n.folder not in FOLDERS:
            warnings.append(f"{rel}: not in a topic folder ({', '.join(FOLDERS)})")
        for p in naming_problems(n.title):
            errors.append(f"{rel}: file name {p}")
        if n.h1 != n.title:
            errors.append(f"{rel}: first heading {n.h1!r} does not match file name")
        if n.meta.get("title") and n.meta["title"] != n.title:
            errors.append(f"{rel}: title property {n.meta['title']!r} does not match file name")
        key = norm(n.title)
        if key in seen:
            errors.append(f"{rel}: duplicate subject of {seen[key]}")
        seen[key] = rel
        raw_refs = [m for m in LINK.finditer(n.body) if m.group(2).startswith("raw/")]
        if not raw_refs:
            errors.append(f"{rel}: no source reference into raw/")
        if n.title.lower() not in index_links:
            errors.append(f"{rel}: not listed in index.md")
        related = re.search(r"^## Related notes\n(.*?)(^## |\Z)", n.body, re.S | re.M)
        if not related or "[[" not in related.group(1):
            warnings.append(f"{rel}: no related-note links")
        if inbound.get(n.title.lower(), 0) == 0:
            warnings.append(f"{rel}: no incoming links from other notes (only the index)")
        if not n.meta.get("reviewed"):
            warnings.append(f"{rel}: not yet reviewed against its sources")

    return {"notes": len(notes), "links": link_count, "broken_or_ambiguous": broken,
            "errors": errors, "warnings": warnings}


# --------------------------------------------------------------------------- rename

def rename_note(old_title: str, new_title: str, settings: config.Settings | None = None) -> list[str]:
    """Rename a note file and update its heading, title property, every incoming link and the catalog."""
    settings = settings or config.load()
    vault = settings.vault
    problems = naming_problems(new_title)
    if problems:
        raise ValueError(f"{new_title!r}: {'; '.join(problems)}")
    matches = [n for n in all_notes(settings) if n.title == old_title]
    if len(matches) != 1:
        raise ValueError(f"expected one note titled {old_title!r}, found {len(matches)}")
    note = matches[0]
    new_path = note.path.with_name(f"{new_title}.md")
    if new_path.exists():
        raise ValueError(f"{new_path.relative_to(vault)} already exists")
    old_rel, new_rel = note.rel(vault), new_path.relative_to(vault).as_posix()
    note.body = re.sub(rf"^# {re.escape(old_title)}$", f"# {new_title}", note.body, count=1, flags=re.M)
    note.meta["title"] = new_title
    history = note.meta.setdefault("previous_names", [])
    history.append(old_title)
    note.path.unlink()
    note.path = new_path
    write_note(note)

    changed = [new_rel]
    pattern = re.compile(r"\[\[" + re.escape(old_title) + r"(#[^\]|]*)?(\|[^\]]*)?\]\]")
    for p in vault.rglob("*.md"):
        if "raw" in p.relative_to(vault).parts:
            continue  # originals are never edited
        text = p.read_text(encoding="utf-8")
        new = pattern.sub(lambda m: f"[[{new_title}{m.group(1) or ''}{m.group(2) or ''}]]", text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            changed.append(p.relative_to(vault).as_posix())

    cat_path = settings.path("data") / "catalog.json"
    if cat_path.exists():
        cat = json.loads(cat_path.read_text())
        for src in cat.get("sources", {}).values():
            src["notes"] = [new_rel if n == old_rel else n for n in src.get("notes", [])]
        if old_rel in cat.get("notes", {}):
            cat["notes"][new_rel] = cat["notes"].pop(old_rel)
            cat["notes"][new_rel]["title"] = new_title
        cat.setdefault("redirects", {})[old_title] = new_title
        cat_path.write_text(json.dumps(cat, indent=2, ensure_ascii=False))
    notes_path = settings.path("data") / "notes.json"
    if notes_path.exists():
        data = json.loads(notes_path.read_text())
        if old_rel in data:
            data[new_rel] = data.pop(old_rel)
            data[new_rel]["title"] = new_title
        for d in data.values():
            for r in d.get("related", []):
                if r.get("title") == old_title:
                    r["title"] = new_title
        notes_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return changed


# --------------------------------------------------------------------------- index + catalog pages

def render_index(settings: config.Settings | None = None) -> None:
    settings = settings or config.load()
    notes = all_notes(settings)
    lines = [
        "# Personal Wiki",
        "",
        "Eason Han's personal wiki: portfolio projects, work and school, and the MBA 290T course. "
        "Each note is one subject, written by local Gemma from the original sources in `raw/` and then "
        "checked against them. Every note lists its sources; see [[Source Catalog]] for where each "
        "original came from.",
        "",
    ]
    for folder in FOLDERS:
        group = sorted((n for n in notes if n.folder == folder), key=lambda n: n.title.lower())
        if not group:
            continue
        lines += [f"## {folder}", "", f"_{FOLDER_BLURB[folder]}_", ""]
        for n in group:
            summary = str(n.meta.get("summary", "")).strip()
            lines.append(f"- [[{n.title}]] — {summary}" if summary else f"- [[{n.title}]]")
        lines.append("")
    lines.append(f"_{len(notes)} notes. Index rebuilt by `wiki ingest` on {datetime.now():%Y-%m-%d}._")
    (settings.vault / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_catalog(catalog: dict, settings: config.Settings | None = None) -> None:
    settings = settings or config.load()
    vault = settings.vault
    rows = []
    for rel_raw, src in sorted(catalog.get("sources", {}).items()):
        origin = src.get("origin", {})
        where = origin.get("url") or (f"{origin['repo']} @ `{origin['commit'][:7]}`" if origin.get("repo") else "local file")
        notes = ", ".join(f"[[{Path(n).stem}]]" for n in src.get("notes", [])) or "—"
        label = rel_raw[:-3] if rel_raw.endswith(".md") else rel_raw
        rows.append(f"| {src.get('title', '')} | [[{label}\\|{Path(rel_raw).name}]] | {origin.get('collection', '')} | "
                    f"{where} | `{src['sha256'][:12]}` | {notes} |")
    text = [
        "# Source Catalog",
        "",
        "Every original in `raw/` is kept byte-for-byte as captured. This table maps each original to its "
        "origin, a checksum (so any change is detectable) and the wiki notes built from it. Machine IDs live "
        "here and in note properties, never in note names.",
        "",
        "| Source | Original file | Collection | Origin | sha256 | Wiki notes |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "Back to [[index]].",
    ]
    (vault / "Source Catalog.md").write_text("\n".join(text) + "\n", encoding="utf-8")
