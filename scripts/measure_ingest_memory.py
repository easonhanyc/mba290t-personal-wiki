"""Memory of the local model servers while ingesting, sampled once per 0.5 s.

With --restart, the Gemma server is restarted first, as for the answer measurement in scripts/measure.py: after
hours idle on a busy Mac, macOS pages most of the model out and `ps` RSS then understates what the model needs.
The ingest runs on a throwaway copy of the project (WIKI_HOME points at it), so the real vault is not touched:
`wiki ingest --force` re-reads one source and calls Gemma as a normal ingest does. Needs `wiki serve start`.

    python scripts/measure_ingest_memory.py --restart   # -> evidence/metrics/ingest-memory.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from wiki import config, serve


def rss_mb(pid: int) -> float | None:
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return round(int(out) / 1024, 1) if out else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="raw/website/artifacts/prioritization-framework.md")
    ap.add_argument("--restart", action="store_true", help="restart the Gemma server first (model freshly resident)")
    args = ap.parse_args()
    root = config.load().root
    swap = lambda: subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout.strip()
    if args.restart:
        serve.stop(("gemma",), log=lambda *_: None)
        serve.start(("gemma",), log=lambda *_: None)
    pids = {n: int((root / "logs" / f"{n}.pid").read_text()) for n in ("gemma", "embed")}
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "project"
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".venv", ".git", "backups", "runs", "logs", "evidence"))
        for d in ("runs", "logs"):
            (copy / d).mkdir()
        before = {n: rss_mb(p) for n, p in pids.items()}
        samples = {n: [] for n in pids}
        start = time.perf_counter()
        proc = subprocess.Popen([str(Path(sys.executable).parent / "wiki"), "ingest", "--force", str(copy / "vault" / args.source)],
                                env={**os.environ, "WIKI_HOME": str(copy)}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while proc.poll() is None:
            for n, p in pids.items():
                if (v := rss_mb(p)) is not None:
                    samples[n].append(v)
            time.sleep(0.5)
        output = proc.stdout.read()
        seconds = round(time.perf_counter() - start, 1)
        record = json.loads(max((copy / "runs").glob("ingest-*.json")).read_text())
    result = {"time": datetime.now().isoformat(timespec="seconds"), "source": args.source, "wall_seconds": seconds,
              "gemma_restarted_first": args.restart, "swap_after": swap(),
              "model_calls": record.get("model_calls"), "exit_code": proc.returncode,
              "rss_mb_before": before, "rss_mb_peak_during": {n: max(v) if v else None for n, v in samples.items()},
              "samples": {n: len(v) for n, v in samples.items()}, "cli_output_tail": output.strip().splitlines()[-4:]}
    dest = root / "evidence" / "metrics" / "ingest-memory.json"
    dest.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k != "cli_output_tail"}, indent=2))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
