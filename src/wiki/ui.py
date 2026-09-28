"""Tiny terminal formatting helpers (ANSI only when writing to a terminal)."""

import os
import sys

_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _wrap(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


def bold(text: str) -> str:
    return _wrap("1", text)


def dim(text: str) -> str:
    return _wrap("2", text)


def warn(text: str) -> str:
    return _wrap("33", text)


def header(command: str, model: str) -> str:
    return dim(f"── wiki {command} · {model} ──")
