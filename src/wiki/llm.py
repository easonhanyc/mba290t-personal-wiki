"""Model clients. The harness talks to Gemma only through these two classes.

LocalGemma  - llama.cpp `llama-server` on this machine (OpenAI-compatible HTTP on 127.0.0.1).
OnlineGemma - hosted Gemma through the Gemini API. Used only when --mode online is given;
              the harness never falls back to it when the local model is unavailable.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlparse

from . import config


class ModelUnavailable(Exception):
    """The requested model cannot be reached. The message says how to fix it."""


class ModelError(Exception):
    """The model answered, but not with something usable."""


@dataclass
class Reply:
    text: str
    model: str
    mode: str
    seconds: float
    timings: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    finish_reason: str = ""


def _post(url: str, body: dict, timeout: float, headers: dict | None = None) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def _get(url: str, timeout: float = 3) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.load(resp)


def assert_local(url: str) -> None:
    host = urlparse(url).hostname
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ModelUnavailable(f"Local mode refuses non-local endpoint {url}; check config/settings.toml.")


class LocalGemma:
    mode = "local"

    def __init__(self, settings: config.Settings | None = None):
        s = (settings or config.load()).local
        self.url = s["url"].rstrip("/")
        self.model_id = s["model_id"]
        self.label = s.get("model_label", self.model_id)
        self.timeout = s.get("timeout_s", 600)
        self.cache_prompt = True  # reuse the KV cache for a shared prompt prefix; measure.py turns it off
        assert_local(self.url)

    def describe(self) -> str:
        return f"{self.model_id} · local · llama.cpp at {self.url}"

    def health(self) -> bool:
        try:
            return _get(f"{self.url}/health").get("status") == "ok"
        except (urllib.error.URLError, OSError, ValueError):
            return False

    def require(self) -> None:
        if not self.health():
            raise ModelUnavailable(
                f"Local Gemma is not running at {self.url}.\n"
                "  Start it with:  wiki serve start\n"
                "  (No cloud fallback is used; local mode needs the local server.)"
            )

    def chat(self, messages: list[dict], max_tokens: int = 400, temperature: float = 0.2,
             schema: dict | None = None) -> Reply:
        self.require()
        body = {"model": self.model_id, "messages": messages, "max_tokens": max_tokens,
                "temperature": temperature, "cache_prompt": self.cache_prompt}
        if schema is not None:
            body["response_format"] = {"type": "json_schema", "json_schema": {"name": "out", "schema": schema}}
        start = time.perf_counter()
        try:
            data = _post(f"{self.url}/v1/chat/completions", body, self.timeout)
        except urllib.error.HTTPError as e:
            raise ModelError(f"llama-server returned HTTP {e.code}: {e.read()[:300]!r}") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise ModelUnavailable(f"Lost connection to local Gemma at {self.url}: {e}") from e
        seconds = time.perf_counter() - start
        try:
            text = data["choices"][0]["message"].get("content") or ""
            finish = data["choices"][0].get("finish_reason") or ""
        except (KeyError, IndexError) as e:
            raise ModelError(f"Unexpected llama-server response: {str(data)[:300]}") from e
        return Reply(text=text.strip(), model=data.get("model", self.model_id), mode=self.mode,
                     seconds=seconds, timings=data.get("timings", {}), usage=data.get("usage", {}),
                     finish_reason=finish)


class OnlineGemma:
    """Hosted Gemma via the Gemini API generateContent endpoint (REST, no SDK)."""

    mode = "online"

    def __init__(self, settings: config.Settings | None = None):
        s = (settings or config.load()).online
        self.endpoint = s["endpoint"].rstrip("/")
        self.model_id = s["model_id"]
        self.key_env = s.get("api_key_env", "GEMINI_API_KEY")
        self.timeout = s.get("timeout_s", 120)
        self.label = f"{self.model_id} (hosted)"

    def describe(self) -> str:
        return f"{self.model_id} · ONLINE · {self.endpoint}"

    def require(self) -> None:
        if not os.environ.get(self.key_env):
            raise ModelUnavailable(
                f"Online mode needs an API key in ${self.key_env}. Create one in Google AI Studio and export it,\n"
                "  or drop --mode online to use the local model (the default)."
            )

    def chat(self, messages: list[dict], max_tokens: int = 400, temperature: float = 0.2,
             schema: dict | None = None) -> Reply:
        self.require()
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                    for m in messages if m["role"] != "system"]
        gen = {"temperature": temperature, "maxOutputTokens": max_tokens, "thinkingConfig": {"thinkingLevel": "minimal"}}
        if schema is not None:
            gen["responseMimeType"] = "application/json"
            gen["responseJsonSchema"] = schema
        body = {"contents": contents, "generationConfig": gen}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        start = time.perf_counter()
        try:
            data = _post(f"{self.endpoint}/{self.model_id}:generateContent", body, self.timeout,
                         headers={"x-goog-api-key": os.environ[self.key_env]})
        except urllib.error.HTTPError as e:
            raise ModelError(f"Gemini API returned HTTP {e.code}: {e.read()[:300]!r}") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise ModelUnavailable(f"Cannot reach the Gemini API (online mode): {e}") from e
        seconds = time.perf_counter() - start
        try:
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        except (KeyError, IndexError) as e:
            raise ModelError(f"Unexpected Gemini API response: {str(data)[:300]}") from e
        return Reply(text=text.strip(), model=data.get("modelVersion", self.model_id), mode=self.mode,
                     seconds=seconds, usage=data.get("usageMetadata", {}))


def get_model(mode: str = "local"):
    if mode == "local":
        return LocalGemma()
    if mode == "online":
        return OnlineGemma()
    raise ValueError(f"Unknown mode {mode!r}; use local or online.")


def parse_json(text: str) -> dict:
    """Parse a JSON object from model output, tolerating code fences."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        t = t[t.find("{"):]
    start, end = t.find("{"), t.rfind("}")
    if start < 0 or end < 0:
        raise ModelError(f"Model did not return JSON: {text[:200]!r}")
    try:
        return json.loads(t[start:end + 1])
    except json.JSONDecodeError as e:
        raise ModelError(f"Model returned malformed JSON ({e}): {text[:200]!r}") from e
