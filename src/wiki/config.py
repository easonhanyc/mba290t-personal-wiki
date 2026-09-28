"""Settings and project paths.

Everything the harness reads or writes is resolved from the project root, found by walking up
from the current directory to the folder that holds config/settings.toml (or $WIKI_HOME).
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    pass


def find_root() -> Path:
    env = os.environ.get("WIKI_HOME")
    if env:
        root = Path(env).expanduser().resolve()
        if (root / "config" / "settings.toml").exists():
            return root
        raise ConfigError(f"WIKI_HOME={env} does not contain config/settings.toml")
    for folder in [Path.cwd(), *Path.cwd().parents]:
        if (folder / "config" / "settings.toml").exists():
            return folder
    # Fall back to the checkout this package was installed from (editable install).
    here = Path(__file__).resolve()
    for folder in here.parents:
        if (folder / "config" / "settings.toml").exists():
            return folder
    raise ConfigError("Could not find config/settings.toml. Run wiki from the project folder or set WIKI_HOME.")


@dataclass
class Settings:
    root: Path
    raw: dict

    def section(self, name: str) -> dict:
        return self.raw.get(name, {})

    def path(self, key: str) -> Path:
        return self.root / self.raw["paths"][key]

    @property
    def vault(self) -> Path:
        return self.path("vault")

    @property
    def local(self) -> dict:
        return self.raw["local"]

    @property
    def online(self) -> dict:
        return self.raw["online"]

    @property
    def retrieval(self) -> dict:
        return self.raw["retrieval"]

    def origins(self) -> list[dict]:
        path = self.root / "config" / "sources.toml"
        if not path.exists():
            return []
        with open(path, "rb") as f:
            return tomllib.load(f).get("origin", [])


_cached: Settings | None = None


def load() -> Settings:
    global _cached
    if _cached is None:
        root = find_root()
        with open(root / "config" / "settings.toml", "rb") as f:
            _cached = Settings(root=root, raw=tomllib.load(f))
    return _cached


def rel(path: Path) -> str:
    """Project-relative POSIX path for display and logs."""
    try:
        return path.resolve().relative_to(load().root).as_posix()
    except ValueError:
        return str(path)
