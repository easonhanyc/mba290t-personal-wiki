"""Turn raw source files into sections of readable text with line numbers.

The raw files are never modified. This module only reads them and produces a cleaned view:
YAML front matter becomes a "properties" section, inline SVG figures are reduced to their
<title> caption, HTML tags are stripped, and every block of text keeps the line number where it
starts in the original file so a citation can point back to it.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

import yaml

SUPPORTED = {".md", ".markdown", ".txt", ".html", ".htm"}


@dataclass
class Block:
    line: int
    end_line: int
    text: str


@dataclass
class Section:
    path: list[str]
    blocks: list[Block] = field(default_factory=list)
    kind: str = "body"  # "properties" for front matter

    @property
    def heading(self) -> str:
        return self.path[-1] if self.path else ""

    @property
    def label(self) -> str:
        return " › ".join(self.path) if self.path else "(introduction)"

    @property
    def words(self) -> int:
        return sum(len(b.text.split()) for b in self.blocks)


@dataclass
class Document:
    path: Path
    title: str
    fmt: str
    properties: dict
    sections: list[Section]

    @property
    def words(self) -> int:
        return sum(s.words for s in self.sections)

    def headings(self) -> set[str]:
        return {s.heading for s in self.sections if s.heading and s.kind == "body"}


# --------------------------------------------------------------------------- markdown

_SKIP_PROPS = {"order", "featured", "live"}


def _prop_text(value) -> str:
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(" ".join(str(v) for v in item.values()))
            else:
                parts.append(str(item))
        return "; ".join(parts)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def _blank_keep_lines(match: re.Match, replacement: str = "") -> str:
    """Replace a multi-line match but keep its newline count so later line numbers stay true."""
    return replacement + "\n" * match.group(0).count("\n")


def _strip_html_blocks(body: str) -> str:
    def svg(m: re.Match) -> str:
        title = re.search(r"<title[^>]*>(.*?)</title>", m.group(0), re.S | re.I)
        caption = f"[Figure: {html.unescape(title.group(1)).strip()}]" if title else ""
        return _blank_keep_lines(m, caption)

    body = re.sub(r"<svg\b.*?</svg>", svg, body, flags=re.S | re.I)
    body = re.sub(r"<(script|style)\b.*?</\1>", _blank_keep_lines, body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", _blank_keep_lines, body, flags=re.S)
    return body


_TAG = re.compile(r"<[^>\n]+>")
_IMG = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def _clean_line(line: str) -> str:
    line = _IMG.sub(lambda m: f"[Image: {m.group(1)}]" if m.group(1) else "", line)
    line = _LINK.sub(r"\1", line)
    line = _TAG.sub(" ", line)
    line = html.unescape(line)
    return re.sub(r"[ \t]+", " ", line).strip()


def parse_markdown(path: Path, text: str) -> Document:
    lines = text.split("\n")
    properties: dict = {}
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                try:
                    loaded = yaml.safe_load("\n".join(lines[1:i])) or {}
                    properties = loaded if isinstance(loaded, dict) else {}
                except yaml.YAMLError:
                    properties = {}
                start = i + 1
                break

    sections: list[Section] = []
    if properties:
        props = Section(path=["Properties"], kind="properties")
        for key, value in properties.items():
            if key in _SKIP_PROPS or value in (None, "", []):
                continue
            props.blocks.append(Block(line=2, end_line=start, text=f"{key}: {_prop_text(value)}"))
        # Front matter is one block so its fields stay together in retrieval.
        if props.blocks:
            merged = "\n".join(b.text for b in props.blocks)
            props.blocks = [Block(line=1, end_line=start, text=merged)]
            sections.append(props)

    body = _strip_html_blocks("\n".join(lines[start:]))
    body_lines = body.split("\n")

    title = str(properties.get("title") or "").strip()
    stack: list[tuple[int, str]] = []
    current = Section(path=[])
    para: list[str] = []
    para_start = 0
    in_code = False

    def flush(end_line: int) -> None:
        nonlocal para
        if para:
            if in_code_block(para):
                joined = "\n".join(para)
            else:
                # List items, table rows and quotes keep their own line; wrapped prose is re-joined.
                joined = para[0]
                for p in para[1:]:
                    sep = "\n" if re.match(r"^(\||[-*+] |> |\d+[.)] )", p) else " "
                    joined += sep + p
            joined = joined.strip()
            if joined:
                current.blocks.append(Block(line=para_start, end_line=end_line, text=joined))
        para = []

    def in_code_block(chunk: list[str]) -> bool:
        return bool(chunk) and chunk[0].startswith("```")

    for offset, raw_line in enumerate(body_lines):
        lineno = start + offset + 1
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            if not in_code:
                flush(lineno - 1)
                in_code = True
                para, para_start = [stripped], lineno
            else:
                para.append(stripped)
                in_code = False
                flush(lineno)
            continue
        if in_code:
            para.append(raw_line.rstrip())
            continue
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", raw_line)
        if heading:
            flush(lineno - 1)
            if current.blocks:
                sections.append(current)
            level = len(heading.group(1))
            text = _clean_line(heading.group(2))
            if level == 1 and not title:
                title = text
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, text))
            current = Section(path=[h for _, h in stack])
            continue
        if not stripped or stripped == "---":
            flush(lineno - 1)
            continue
        cleaned = _clean_line(raw_line)
        if not cleaned:
            continue
        # Table rows and list items stay on their own lines inside a block.
        if not para:
            para_start = lineno
        para.append(cleaned)
    flush(len(lines))
    if current.blocks:
        sections.append(current)

    if not title and properties.get("org"):
        title = str(properties["org"])  # experience entries have an org and role, not a title
    return Document(path=path, title=title or path.stem, fmt="markdown", properties=properties, sections=sections)


# --------------------------------------------------------------------------- html

class _HtmlSections(HTMLParser):
    SKIP = {"script", "style", "svg", "nav", "noscript", "template", "button"}
    BLOCK = {"p", "li", "tr", "div", "section", "article", "blockquote", "pre", "dt", "dd", "br", "table", "ul", "ol"}
    HEAD = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.stack: list[tuple[int, str]] = []
        self.sections: list[Section] = [Section(path=[])]
        self.buf: list[str] = []
        self.buf_line = 0
        self.heading_level = 0
        self.heading_buf: list[str] = []
        self.title = ""
        self.in_title = False

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            line = self.buf_line or self.getpos()[0]
            self.sections[-1].blocks.append(Block(line=line, end_line=self.getpos()[0], text=text))
        self.buf = []
        self.buf_line = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
        if tag in self.HEAD:
            self._flush()
            self.heading_level = self.HEAD[tag]
            self.heading_buf = []
        elif tag in self.BLOCK:
            self._flush()
        elif tag in ("td", "th"):
            self.buf.append(" | ")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        if tag in self.HEAD and self.heading_level:
            text = re.sub(r"\s+", " ", "".join(self.heading_buf)).strip()
            level = self.heading_level
            self.heading_level = 0
            if text:
                while self.stack and self.stack[-1][0] >= level:
                    self.stack.pop()
                self.stack.append((level, text))
                self.sections.append(Section(path=[h for _, h in self.stack]))
        elif tag in self.BLOCK:
            self._flush()

    def handle_data(self, data):
        if self.in_title:
            self.title += data
            return
        if self.skip_depth:
            return
        if self.heading_level:
            self.heading_buf.append(data)
            return
        if data.strip() and not self.buf_line:
            self.buf_line = self.getpos()[0]
        self.buf.append(data)


def parse_html(path: Path, text: str) -> Document:
    parser = _HtmlSections()
    parser.feed(text)
    parser._flush()
    sections = [s for s in parser.sections if s.blocks]
    title = re.sub(r"\s+", " ", parser.title).strip() or path.stem
    return Document(path=path, title=title, fmt="html", properties={}, sections=sections)


# --------------------------------------------------------------------------- entry points

def parse_file(path: Path) -> Document:
    text = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        return parse_html(path, text)
    return parse_markdown(path, text)


def render(doc: Document, sections: list[Section] | None = None, short: bool = False) -> str:
    """Readable text of a document (or some of its sections) for a model prompt.

    short=True labels each section with its own heading only (fewer tokens to copy into JSON)."""
    out = []
    for s in sections if sections is not None else doc.sections:
        out.append(f"## {(s.heading or s.label) if short else s.label}")
        out.extend(b.text for b in s.blocks)
        out.append("")
    return "\n".join(out).strip()
