"""Start, stop and inspect the two local llama-server processes.

  gemma  : the chat/answer model   (127.0.0.1:8080)
  embed  : EmbeddingGemma vectors  (127.0.0.1:8081)

Both bind to 127.0.0.1 only. PIDs are kept in logs/*.pid so `wiki serve stop` can find them.
"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

from . import config
from .embed import Embedder
from .llm import LocalGemma


def _commands(settings: config.Settings) -> dict[str, list[str]]:
    s = settings.local
    g, e = urlparse(s["url"]), urlparse(s["embed_url"])
    return {
        "gemma": ["llama-server", "-m", str(Path(s["model_file"]).expanduser()), "-a", s["model_id"],
                  "-c", str(s["ctx"]), "-np", "1", "-ngl", "99", "--reasoning", "off", "--no-webui",
                  "--host", g.hostname, "--port", str(g.port)],
        "embed": ["llama-server", "-m", str(Path(s["embed_model_file"]).expanduser()), "-a", s["embed_model_id"],
                  "--embedding", "-c", str(s["embed_ctx"]), "-b", str(s["embed_ctx"]), "-ub", str(s["embed_ctx"]),
                  "-np", "1", "-ngl", "99", "--no-webui", "--host", e.hostname, "--port", str(e.port)],
    }


def _pidfile(settings: config.Settings, name: str) -> Path:
    d = settings.path("logs")
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{name}.pid"


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _pid(settings: config.Settings, name: str) -> int | None:
    f = _pidfile(settings, name)
    if f.exists():
        try:
            pid = int(f.read_text().strip())
            if _alive(pid):
                return pid
        except ValueError:
            pass
    return None


def _healthy(settings: config.Settings, name: str) -> bool:
    return LocalGemma(settings).health() if name == "gemma" else Embedder(settings).available()


def start(names=("gemma", "embed"), wait: float = 180, log=print) -> bool:
    settings = config.load()
    if not shutil.which("llama-server"):
        log("llama-server not found. Install the runtime with:  brew install llama.cpp")
        return False
    cmds = _commands(settings)
    ok = True
    for name in names:
        if _healthy(settings, name):
            log(f"  {name}: already running")
            continue
        model = Path(cmds[name][2])
        if not model.exists():
            log(f"  {name}: model file missing: {model}\n    See README 'Setup' for the official download command.")
            ok = False
            continue
        logfile = open(settings.path("logs") / f"{name}-server.log", "a")
        proc = subprocess.Popen(cmds[name], stdout=logfile, stderr=subprocess.STDOUT, start_new_session=True)
        _pidfile(settings, name).write_text(str(proc.pid))
        log(f"  {name}: starting (pid {proc.pid}) ...")
    for name in names:
        deadline = time.time() + wait
        while time.time() < deadline and not _healthy(settings, name):
            time.sleep(1)
        healthy = _healthy(settings, name)
        ok &= healthy
        log(f"  {name}: {'ready' if healthy else 'NOT ready (see logs/' + name + '-server.log)'}")
    return ok


def stop(names=("gemma", "embed"), log=print) -> None:
    settings = config.load()
    for name in names:
        pid = _pid(settings, name)
        if pid is None:
            log(f"  {name}: not running (no pid file)")
            continue
        os.kill(pid, signal.SIGTERM)
        for _ in range(50):
            if not _alive(pid):
                break
            time.sleep(0.1)
        _pidfile(settings, name).unlink(missing_ok=True)
        log(f"  {name}: stopped (pid {pid})")


def status() -> dict:
    settings = config.load()
    out = {}
    for name in ("gemma", "embed"):
        out[name] = {"healthy": _healthy(settings, name), "pid": _pid(settings, name),
                     "url": settings.local["url" if name == "gemma" else "embed_url"]}
    return out
