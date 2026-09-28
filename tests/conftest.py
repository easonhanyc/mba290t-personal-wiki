"""Test fixtures: a throwaway project folder and a fake model, so harness logic is tested without Gemma."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from wiki import config, retrieval
from wiki.llm import Reply

ROOT = Path(__file__).resolve().parents[1]


class FakeModel:
    """Stands in for LocalGemma. `responses` maps a key to text; the key is chosen by `pick`."""

    model_id = "fake-gemma"
    mode = "local"

    def __init__(self, pick=None):
        self.calls: list[dict] = []
        self.pick = pick or (lambda messages, schema: "ok")

    def require(self):
        return None

    def describe(self):
        return "fake-gemma · local"

    def chat(self, messages, max_tokens=400, temperature=0.2, schema=None):
        self.calls.append({"messages": messages, "schema": schema})
        text = self.pick(messages, schema)
        if not isinstance(text, str):
            text = json.dumps(text)
        return Reply(text=text, model=self.model_id, mode=self.mode, seconds=0.01, timings={"prompt_n": 10, "predicted_n": 5})


class NoEmbedder:
    def __init__(self, *a, **k):
        pass

    def available(self):
        return False


@pytest.fixture
def project(tmp_path, monkeypatch):
    for d in ("config", "instructions"):
        shutil.copytree(ROOT / d, tmp_path / d)
    for d in ("vault/raw", "vault/wiki", "data", "runs", "logs"):
        (tmp_path / d).mkdir(parents=True)
    monkeypatch.setenv("WIKI_HOME", str(tmp_path))
    monkeypatch.setattr(config, "_cached", None)
    monkeypatch.setattr(retrieval, "Embedder", NoEmbedder)
    yield tmp_path
    config._cached = None
