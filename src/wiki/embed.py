"""EmbeddingGemma client (a second llama-server started with --embedding).

EmbeddingGemma expects task prefixes: queries and documents are embedded differently.
Vectors are L2-normalised so a dot product is cosine similarity.
"""

from __future__ import annotations

import urllib.error

import numpy as np

from . import config
from .llm import _get, _post, assert_local

QUERY_PREFIX = "task: search result | query: "


def doc_text(title: str, text: str) -> str:
    return f"title: {title or 'none'} | text: {text}"


class Embedder:
    def __init__(self, settings: config.Settings | None = None):
        s = (settings or config.load()).local
        self.url = s["embed_url"].rstrip("/")
        self.model_id = s["embed_model_id"]
        assert_local(self.url)

    def available(self) -> bool:
        try:
            return _get(f"{self.url}/health").get("status") == "ok"
        except (urllib.error.URLError, OSError, ValueError):
            return False

    def embed(self, texts: list[str], batch: int = 16) -> np.ndarray:
        rows = []
        for i in range(0, len(texts), batch):
            data = _post(f"{self.url}/v1/embeddings", {"model": self.model_id, "input": texts[i:i + batch]}, 300)
            ordered = sorted(data["data"], key=lambda d: d["index"])
            rows.extend(d["embedding"] for d in ordered)
        arr = np.asarray(rows, dtype=np.float32)
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        return arr / np.maximum(norms, 1e-12)

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed([QUERY_PREFIX + query])[0]
