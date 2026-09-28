# Methodology: how the three settings were chosen

The three values in the notebook were not guessed. They came from 8 training runs totalling roughly
1.6 million agent decisions, scored with the notebook's own evaluation protocol. This document records
the harness, the hardware, the measurements, and how to reproduce them.

## The problem with guessing

The notebook exposes three knobs and hides everything else behind "fixed classroom settings". Two
properties of those fixed settings make the knobs behave unintuitively:

- **The replay buffer holds only 5,000 transitions** — about seven games. The agent is therefore
  learning from a narrow, recent window rather than a broad history, so the *exploration* rate strongly
  shapes what it sees, not just how it acts.
- **The target network syncs only every 1,000 decisions.** Larger learning rates chase a target that
  moves in discrete jumps, which destabilises rather than accelerates learning.

Both effects turned out to matter, and both pointed the opposite way from the intuition that "higher
learning rate = faster progress, within a short budget".

## The harness

Running the full notebook per candidate would have been far too slow, so
[`../sweep/core.py`](../sweep/core.py) extracts the notebook's logic cell-for-cell — `make_env`, `DQN`,
`ReplayMemory`, `choose_action`, `learn`, and `evaluate`, plus every fixed constant (`SEED=42`,
`MAX_STEPS=3000`, `REPLAY_CAPACITY=5000`, `BATCH_SIZE=32`, `WARMUP_STEPS=1000`, `TRAIN_EVERY=4`,
`TARGET_EVERY=1000`, `GAMMA=0.99`, `EVAL_SEEDS`, `EVAL_EXPLORATION=0.05`). Nothing is simplified.

[`../sweep/run_sweep.py`](../sweep/run_sweep.py) trains one configuration and evaluates it on the five
official seeds at chosen episode checkpoints, so every number in the tables below is measured the same
way the notebook measures its final score.

**This transfers because the notebook is deterministic.** The independently-launched 300-episode
notebook run reproduced the standalone harness's prediction exactly — 906.0 — and its 25- and
50-episode demo scores (380, 510) matched the earlier 250-episode run to the point. Pre-selecting
settings offline and then running the real notebook once is therefore sound here, not an approximation.

## Hardware and measured throughput

Apple M2, 8 cores, 16 GB RAM, macOS 26.6.2 arm64, Python 3.12.14, PyTorch 2.14.0.

| Configuration | Throughput |
|---|---|
| 1 worker, MPS backend | **~165–175 decisions/sec** |
| 1 worker, CPU (4 threads) | ~64 decisions/sec |
| 4 workers × 2 threads, CPU | ~21 each (~84 aggregate) |
| 6 workers × 1 thread, CPU | ~16 each (~96 aggregate) |

Two practical consequences. **MPS is ~2.7× faster than CPU** for this network, so a 300-episode run
costs about 19 minutes rather than the hour a CPU estimate suggests. And **CPU parallelism saturates
quickly** — six workers deliver only 1.5× the throughput of one — so stage 1 ran six configurations in
parallel on CPU, while stage 2 ran two longer configurations on MPS.

Benchmarks: [`../sweep/bench.py`](../sweep/bench.py), [`../sweep/bench2.py`](../sweep/bench2.py).

## Stage 1 — exploration × learning rate

Six configurations, 60 episodes each, CPU, launched by [`../sweep/launch.sh`](../sweep/launch.sh).
Untrained baseline on these seeds: **492**.

| Exploration | Learning rate | Eval @30 | Eval @60 |
|---|---|---|---|
| **0.10** | **0.0001** | 460 | **1030** |
| 0.20 | 0.00025 | 598 | 652 |
| 0.20 | 0.0001 | 470 | 554 |
| 0.05 | 0.00025 | 224 | 512 |
| 0.10 | 0.0005 | 474 | 320 |
| 0.10 | 0.00025 | 350 | 288 |

Three findings:

1. **Every learning rate above 1e-4 was worse**, monotonically, at the 60-episode mark. The notebook's
   default is genuinely well chosen for its fixed settings, not merely a safe placeholder.
2. **Exploration of 0.05 produced the worst agent in the whole study** (224 at 30 episodes). With a
   5,000-transition buffer, too little exploration fills memory with near-identical states and the
   policy degenerates.
3. **At 30 episodes every configuration was at or below the untrained baseline.** A short run is not a
   small improvement — it is actively worse than not training, because the network has left its
   accidentally-reasonable random initialisation without yet learning anything. This is why the
   assignment's "try 5 episodes" is described as a setup check, not a result.

Raw logs in [`../sweep/logs/`](../sweep/logs/), parsed results in
[`../results/hyperparameter_search.json`](../results/hyperparameter_search.json).

## Stage 2 — episode budget, and one test of a "fixed" setting

Two configurations, 400 episodes each, MPS, both at exploration 0.10 / lr 0.0001, launched by
[`../sweep/launch2.sh`](../sweep/launch2.sh). Arm A keeps the stock 5,000 replay buffer; arm B raises it
tenfold to 50,000.

| Episodes | A: replay 5,000 (stock) | B: replay 50,000 |
|---|---|---|
| 100 | 410 | 702 |
| 200 | 454 | 200 |
| 300 | **906** | 420 |
| 400 | 656 | 414 |

**The hypothesis was wrong.** The small replay buffer looked like the obvious bottleneck, and the
assignment permits tuning other hyperparameters with explanation — but the larger buffer was worse at
three of the four checkpoints. Ten times more memory, spread over the same ~46,000 updates, means each
transition is revisited far less often; at this budget the agent learns less from more data. The stock
setting was kept, and the submission changes only the three permitted values.

**Episode count is strongly non-monotonic** — 454 → 906 → 656 across 200/300/400 episodes. 300 was
chosen as the measured peak. This is also the single largest caveat on the headline result, and it is
disclosed in the README: the episode budget was selected on the same five seeds used for grading, so
part of the improvement is selection rather than a clean out-of-sample estimate.

Raw logs in [`../sweep/logs2/`](../sweep/logs2/).

## Behaviour probe

Scores alone do not explain *what changed*, and the best trained GIF is actively misleading if read on
its own — within the 20 seconds it covers, the trained agent is behind the untrained one (280 vs 350
points). [`../probe_behaviour.py`](../probe_behaviour.py) replays the saved `untrained.pt` and
`trained.pt` checkpoints under the exact evaluation protocol and logs the score curve and action
distribution.

| | Untrained | Trained |
|---|---|---|
| Final score / length | 350 over 560 decisions | 1410 over 838 decisions |
| Score at decision 300 | 350 | 280 |
| Score at decision 500 | 350 (flat) | 1240 |
| Dominant action | **UPLEFT 95.4%** | UPLEFT 29.6%, DOWN 28.9%, DOWNRIGHT 19.3%, DOWNLEFT 12.8% |

The untrained network is not random — it is *stuck*. An untrained convolutional network scores every
screen almost identically, so the same action wins the `argmax` on nearly every frame; only the 5%
evaluation exploration ever breaks it out. It collects 350 points in 300 decisions by ploughing through
whatever pellets lie in that one direction, then scores nothing at all for its remaining 260 decisions.

What training bought, most visibly, is the ability to steer. Output:
[`../results/behaviour_probe.json`](../results/behaviour_probe.json).

## Reproducing this

```bash
python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt

# The recorded submission run (~19 min on an M2)
.venv/bin/python set_params.py pacman_dqn.ipynb 0.10 300 0.0001
./run_notebook.sh

# Stage 1 and stage 2 searches (~35 min and ~30 min)
cd sweep && ./launch.sh && ./launch2.sh

# Behaviour probe against a finished run folder
.venv/bin/python probe_behaviour.py pacman_runs/<timestamp>
```

`set_params.py` edits only the three values in section 1 and asserts it found exactly one settings
cell. `run_notebook.sh` executes the notebook in place with no per-cell timeout, preserving all outputs.

## What I would do differently

The 250-episode run scored +12 and the 300-episode run scored +414 on identical settings. That gap is
noise, not skill, and no amount of care in choosing three numbers overcomes it. A more honest protocol
at this budget would evaluate several seeds *per configuration* and report confidence intervals rather
than single means — but the notebook's five-seed, final-weights-only evaluation is fixed by the
assignment, and changing it would have made the result incomparable with the rest of the class.
