"""Measure memory use and response time of the local setup on this machine.

    python scripts/measure.py --label local --repeats 3

1. Stops both servers, samples system memory, restarts Gemma with verbose logging so llama.cpp prints
   its own memory breakdown (Metal buffers vs host-mapped weights, KV cache, compute buffers).
2. Runs each ask-mode test question `repeats` times with prompt caching OFF (every run pays full
   prompt processing), sampling the servers' resident memory while they work.
3. Reads ingestion timings from the saved ingest records in runs/.
Writes evidence/metrics/<label>.json and .md. Numbers are measured, never typed in.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import yaml

from wiki import config, harness, retrieval, serve
from wiki.llm import LocalGemma

PAGE = 16384


def vm_used_gb() -> float:
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    pages = {m.group(1): int(m.group(2)) for m in re.finditer(r'^"?(.+?)"?:\s+(\d+)\.', out, re.M)}
    used = pages.get("Pages active", 0) + pages.get("Pages wired down", 0) + pages.get("Pages occupied by compressor", 0)
    return round(used * PAGE / 2**30, 2)


def swap_used_mb() -> float:
    out = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", out)
    return float(m.group(1)) if m else -1.0


def proc_mem(pid: int) -> dict:
    rss = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    fp = subprocess.run(["footprint", str(pid)], capture_output=True, text=True).stdout
    m = re.search(r"phys_footprint:\s+([\d.]+)\s*([KMG]B)", fp)
    footprint_mb = None
    if m:
        footprint_mb = float(m.group(1)) * {"KB": 1 / 1024, "MB": 1, "GB": 1024}[m.group(2)]
    return {"rss_mb": round(int(rss) / 1024, 1) if rss else None, "phys_footprint_mb": footprint_mb}


class Sampler(threading.Thread):
    def __init__(self, pids: dict[str, int], every: float = 1.0):
        super().__init__(daemon=True)
        self.pids, self.every, self.peak, self.stop_flag = pids, every, {}, False

    def run(self):
        while not self.stop_flag:
            for name, pid in self.pids.items():
                m = proc_mem(pid)
                cur = self.peak.setdefault(name, {"rss_mb": 0, "phys_footprint_mb": 0})
                for k in cur:
                    if m.get(k) is not None:
                        cur[k] = max(cur[k], m[k])
            time.sleep(self.every)


def llama_breakdown(log: Path) -> dict:
    """llama.cpp's own memory accounting: the fit projection at load and the actual buffers at shutdown.

    On Apple Silicon the model file is memory-mapped: the Metal buffer maps the whole file and the CPU buffer
    maps the per-layer embedding tables inside it, so the two views share physical pages and must not be added.
    """
    text = log.read_text(errors="replace")
    rows = re.findall(r"- (MTL0 \(Apple M2\)|Host)\s+\|[^|]*?(\d+) =\s+(\d+) \+\s+(\d+) \+\s+(\d+)", text)
    out: dict = {}
    snaps = []
    for name, total, model, ctx, compute in rows:
        dev = "gpu" if name.startswith("MTL0") else "host"
        if dev == "gpu" and (not snaps or "gpu" in snaps[-1]):
            snaps.append({})
        snaps[-1][dev] = {"self_mib": int(total), "model_mib": int(model), "context_mib": int(ctx), "compute_mib": int(compute)}
    if snaps:
        out["projected_at_load"] = snaps[0]
        out["actual_at_shutdown"] = snaps[-1]
    m = re.search(r"offloaded (\d+)/(\d+) layers to GPU", text)
    if m:
        out["layers_on_gpu"] = f"{m.group(1)}/{m.group(2)}"
    return out


def ingest_timings(settings) -> list[dict]:
    rows = []
    for f in sorted(glob.glob(str(settings.path("runs") / "ingest-*.json"))):
        d = json.loads(Path(f).read_text())
        if not d.get("calls"):
            continue
        per_source: dict[str, float] = {}
        for c in d["calls"]:
            per_source[c["source"]] = per_source.get(c["source"], 0) + c["seconds"]
        ingested = [k for k, v in d["files"].items() if v == "ingested"]
        rows.append({"record": config.rel(Path(f)), "time": d["time"], "files_ingested": len(ingested),
                     "files_unchanged": sum(1 for v in d["files"].values() if v == "unchanged"),
                     "wall_seconds": d["seconds"], "model_calls": len(d["calls"]),
                     "prompt_tokens": sum(c.get("prompt_tokens") or 0 for c in d["calls"]),
                     "output_tokens": sum(c.get("output_tokens") or 0 for c in d["calls"]),
                     "per_source_seconds": {k: round(v, 1) for k, v in per_source.items()}})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="local")
    ap.add_argument("--repeats", type=int, default=3)
    args = ap.parse_args()
    settings = config.load()
    out: dict = {"label": args.label, "time": datetime.now().isoformat(timespec="seconds")}

    serve.stop()
    time.sleep(3)
    out["system_before"] = {"used_gb": vm_used_gb(), "swap_used_mb": swap_used_mb()}
    # Start Gemma once with verbose logging to capture llama.cpp's memory accounting.
    cmd = serve._commands(settings)["gemma"] + ["-lv", "4"]
    log = settings.path("logs") / "measure-gemma.log"
    t0 = time.perf_counter()
    with open(log, "w") as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
    serve._pidfile(settings, "gemma").write_text(str(proc.pid))
    gemma = LocalGemma(settings)
    while not gemma.health():
        time.sleep(0.5)
    out["gemma_load_seconds"] = round(time.perf_counter() - t0, 1)
    serve.start(("embed",), log=lambda *_: None)
    time.sleep(2)
    pids = {name: info["pid"] for name, info in serve.status().items()}
    out["llama_cpp_breakdown_log"] = config.rel(log)
    out["after_load"] = {"system_used_gb": vm_used_gb(), "swap_used_mb": swap_used_mb(),
                         **{name: proc_mem(pid) for name, pid in pids.items()}}

    tests = yaml.safe_load((settings.root / "tests" / "questions.yaml").read_text())["ask_tests"]
    index = retrieval.Index(settings)
    gemma.cache_prompt = False
    sampler = Sampler(pids)
    sampler.start()
    runs = []
    for rep in range(args.repeats):
        for t in tests:
            r = harness.ask(t["question"], model=gemma, index=index, save=False)
            tm = r.timings
            runs.append({"test": t["id"], "repeat": rep + 1, "total_s": tm["total_s"], "retrieval_s": tm["retrieval_s"],
                         "model_s": tm.get("model_s"), "prompt_tokens": tm.get("llama_prompt_n"),
                         "prompt_tok_s": round(tm.get("llama_prompt_per_second", 0), 1),
                         "answer_tokens": tm.get("llama_predicted_n"),
                         "gen_tok_s": round(tm.get("llama_predicted_per_second", 0), 1)})
            print(f"  {t['id']} rep {rep + 1}: {tm['total_s']}s")
    sampler.stop_flag = True
    sampler.join(timeout=5)
    out["during_asks_peak"] = sampler.peak
    out["after_asks"] = {"system_used_gb": vm_used_gb(), "swap_used_mb": swap_used_mb()}
    out["ask_runs"] = runs
    out["ask_summary"] = {
        "runs": len(runs), "median_total_s": statistics.median(r["total_s"] for r in runs),
        "min_total_s": min(r["total_s"] for r in runs), "max_total_s": max(r["total_s"] for r in runs),
        "median_retrieval_s": statistics.median(r["retrieval_s"] for r in runs),
        "median_prompt_tok_s": statistics.median(r["prompt_tok_s"] for r in runs),
        "median_gen_tok_s": statistics.median(r["gen_tok_s"] for r in runs),
        "per_test_median_s": {t["id"]: statistics.median(r["total_s"] for r in runs if r["test"] == t["id"]) for t in tests},
    }
    out["ingest"] = ingest_timings(settings)

    # CLI process overhead (Python + index + numpy), measured with /usr/bin/time -l on a search.
    wiki_bin = str(Path(sys.executable).parent / "wiki")
    res = subprocess.run(["/usr/bin/time", "-l", wiki_bin, "search", "row level security", "--json"],
                         capture_output=True, text=True, cwd=settings.root)
    m = re.search(r"(\d+)\s+maximum resident set size", res.stderr)
    w = re.search(r"([\d.]+) real", res.stderr)
    out["cli_search_process"] = {"peak_rss_mb": round(int(m.group(1)) / 2**20, 1) if m else None,
                                 "wall_s": float(w.group(1)) if w else None}

    # Restart Gemma normally; stopping it makes llama.cpp print its actual memory accounting to the log.
    serve.stop(("gemma",), log=lambda *_: None)
    time.sleep(2)
    out["llama_cpp_breakdown"] = llama_breakdown(log)
    serve.start(("gemma",), log=lambda *_: None)

    dest = settings.root / "evidence" / "metrics"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{args.label}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ("llama_cpp_breakdown", "after_load", "during_asks_peak", "ask_summary", "cli_search_process")}, indent=1))


def first_start_seconds(settings) -> float | None:
    """Seconds from launch to 'model loaded' in the very first llama-server start (cold disk cache)."""
    log = settings.root / "evidence" / "metrics" / "first-start-gemma-server.log"
    if not log.exists():
        return None
    m = re.search(r"^(\d+)\.(\d+)\.(\d+)\.\d+ I srv  llama_server: model loaded", log.read_text(), re.M)
    return round(int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) / 1000, 1) if m else None
    return 0


if __name__ == "__main__":
    sys.exit(main())
