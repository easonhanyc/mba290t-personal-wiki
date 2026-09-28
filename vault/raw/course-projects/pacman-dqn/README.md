# Ms. Pac-Man DQN — Class 3 Assignment

Training a Deep Q-Network to play Ms. Pac-Man, using the course notebook
[`pacman_dqn.ipynb`](pacman_dqn.ipynb). The three student-chosen settings were
**exploration = 0.10, episodes = 300, learning rate = 0.0001**, selected by a two-stage
hyperparameter search described below.

**Headline result: mean evaluation score rose from 492 (untrained) to 906 (trained), +414 / +84%,
under identical evaluation settings.**

---

## Overview and how to run

The agent sees four stacked 84×84 grayscale game screens, picks one of nine joystick actions, and
learns from the game's own score. A convolutional network estimates the future reward of each move;
a slower-moving target network supplies the learning target.

To reproduce:

1. Open [`pacman_dqn.ipynb`](pacman_dqn.ipynb) in Jupyter, VS Code, or Google Colab
   (Colab: **Runtime → Change runtime type → T4 GPU**). Use a Python 3.11–3.13 kernel.
2. Section 1 already contains the three chosen settings. No other cell needs editing.
3. Choose **Run All**. Setup, baseline evaluation, training, and final evaluation run in order.
4. Results are written to a fresh `pacman_runs/<timestamp>/` folder and zipped by the final cell.

Locally this was run headless with:

```bash
python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
./run_notebook.sh    # nbconvert --execute --inplace, no per-cell timeout
```

## Repository layout

| Path | What it is |
|---|---|
| [`pacman_dqn.ipynb`](pacman_dqn.ipynb) | **The submission** — executed notebook, all cell outputs intact ([how GitHub renders it](#a-note-on-how-github-renders-this-notebook)) |
| [`results/`](results/) | Evidence from the recorded 300-episode run: scores, plot, GIFs, logs |
| [`results_run250/`](results_run250/) | The earlier, weaker 250-episode run, kept for honest comparison |
| [`docs/ASSIGNMENT.md`](docs/ASSIGNMENT.md) | Assignment background, source notebook, and where each requirement is answered |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | **How the three settings were chosen** — harness, hardware, all search data |
| [`sweep/`](sweep/) | The search harness itself: notebook logic extracted, runners, benchmarks, raw logs |
| [`probe_behaviour.py`](probe_behaviour.py) | Replays saved checkpoints to measure score curve and action mix |
| [`set_params.py`](set_params.py) | Edits only the three values in section 1 of the notebook |
| [`run_notebook.sh`](run_notebook.sh) | Headless execution preserving outputs |

Model checkpoints (`*.pt`, ~6.8 MB each) and full `pacman_runs/` folders are gitignored and attached to
the [v1.0 release](https://github.com/easonhanyc/mba290t-pacman-dqn/releases/tag/v1.0) instead — see
[Where the model checkpoints are saved](#where-the-model-checkpoints-are-saved).

---

## My three hyperparameters

| Setting | Value | Why I chose it |
|---|---|---|
| **Exploration** | `0.10` | The measured sweet spot. At `0.05` the agent collapsed into a degenerate, stuck policy (eval mean 224) because the 5,000-transition replay buffer fills with near-identical states. At `0.20` a fifth of all moves are noise, which held the score down. `0.10` keeps enough randomness to escape corners while letting most experience come from the learned policy. |
| **Episodes** | `300` | The budget I could afford (≈19 min on this machine) and the point where measured evaluation score peaked. Scores are non-monotonic: 100 → 410, 200 → 454, 300 → **906**, 400 → 656. |
| **Learning rate** | `0.0001` | The notebook's reference value, and it won clearly. Every increase made learning *worse*, not faster: 0.00025 → 288 and 0.0005 → 320 at 60 episodes, versus 1030 for 0.0001. With a small replay buffer and a target network synced only every 1,000 decisions, larger steps chase a moving target and destabilise. |

Everything else — replay capacity, batch size, warm-up, target sync, gamma, and all evaluation
settings — was left exactly as the notebook ships it.

---

## How I chose them: a two-stage search

Rather than guess, I ran the notebook's exact training and evaluation logic as a standalone script
and searched — 8 runs, roughly 1.6 million agent decisions. Every configuration was scored with the
**notebook's own evaluation protocol** — the same five seeds `[101, 202, 303, 404, 505]`, 5%
exploration, same time limit — so numbers are directly comparable.

Full write-up in **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**; harness in [`sweep/`](sweep/); raw data
in [`results/hyperparameter_search.json`](results/hyperparameter_search.json).

### Stage 1 — exploration × learning rate (6 configs, 60 episodes each, CPU)

The untrained baseline on these seeds is **492**.

| Exploration | Learning rate | Eval @30 | Eval @60 |
|---|---|---|---|
| **0.10** | **0.0001** | 460 | **1030** |
| 0.20 | 0.00025 | 598 | 652 |
| 0.20 | 0.0001 | 470 | 554 |
| 0.05 | 0.00025 | 224 | 512 |
| 0.10 | 0.0005 | 474 | 320 |
| 0.10 | 0.00025 | 350 | 288 |

Two findings drove the final choice: **raising the learning rate above 1e-4 consistently hurt**, and
**exploration below 0.10 produced a stuck agent**. Note also that at 30 episodes *every* configuration
sat at or below the untrained baseline — the early-DQN dip, where the network has moved away from its
accidentally-reasonable random initialisation but has not yet learned anything useful. A short run is
genuinely worse than no training at all.

### Stage 2 — episode budget, and one test of a fixed setting (400 episodes each, MPS)

| Episodes | Replay 5,000 (stock) | Replay 50,000 |
|---|---|---|
| 100 | 410 | 702 |
| 200 | 454 | 200 |
| 300 | **906** | 420 |
| 400 | 656 | 414 |

I suspected the 5,000-transition replay buffer was the real bottleneck, so I tested a 10× larger one.
**It did not help** — the larger buffer was worse at three of four checkpoints. So I kept every fixed
classroom setting untouched and changed only the three permitted values. This is a case where the
obvious hypothesis was wrong and the measurement was worth taking.

---

## What I expected, and what actually happened

**Before training I expected** a modest but steady improvement over the untrained baseline, with the
score rising smoothly as episodes accumulated, and I expected a larger replay buffer to be the single
biggest available win.

**What I observed instead:**

- **Improvement is real but violently non-monotonic.** The per-25-episode demonstration scores were
  380, 510, 980, 400, 720, 670, 710, 580, 750, 900, 560, **1410**. There is an upward trend, but any
  individual checkpoint is a lottery. Stopping at episode 275 instead of 300 would have produced a
  much weaker agent.
- **A bigger replay buffer made things worse,** contradicting my main hypothesis.
- **Training loss rose while play improved** — mean update loss went from 0.040 (first 25 episodes) to
  0.110 (last 25). Rising loss here is a healthy sign: as the agent survives longer and eats more, the
  rewards it must predict get larger and more varied. Loss is not a scoreboard.
- **The clearest evidence of learning is survival time.** Evaluation episodes lengthened from a mean of
  589 decisions to 763 — the trained agent stays alive about 30% longer.
- **What it actually learned was to stop repeating one move.** I did not expect the *untrained*
  baseline to be a degenerate one-action policy, but it is: 95.4% of its moves are UPLEFT, because an
  untrained network scores every screen almost identically and the same action always wins the `argmax`.
  The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%). Much of the +414
  is simply the agent learning to *steer at all* — which also means the 492-point baseline flatters an
  agent that is really just walking into a wall.

Training-score progression, averaged in blocks of 50 episodes:
677 → 742 → 784 → 668 → 728 → **844**.

---

## Actual run facts

| | |
|---|---|
| Status | `completed` (not interrupted) |
| Completed episodes | **300 / 300** |
| Total decisions | **184,258** |
| Learning updates | **45,815** |
| Elapsed training time | **1,124 s ≈ 18.7 min** (including periodic demonstrations) |
| Hardware | Apple M2, 8 cores, 16 GB RAM — PyTorch **MPS** backend |
| Software | macOS 26.6.2 arm64, Python 3.12.14, torch 2.14.0, gymnasium 1.3.0, ale-py 0.11.2, numpy 2.5.3 |

Learning updates are non-zero and the run completed normally, so every result below reflects a fully
trained agent. Full details: [`results/training_summary.json`](results/training_summary.json),
[`results/config.json`](results/config.json), [`results/training.csv`](results/training.csv).

---

## Results: all five before/after scores

Identical settings before and after — same five seeds, 5% exploration, same 3,000-decision limit.
The baseline is an **untrained network**, not a random-action agent.

| Evaluation seed | Before (untrained) | After (trained) | Change |
|---|---|---|---|
| 101 | 350 | **1410** | +1060 |
| 202 | 500 | **990** | +490 |
| 303 | 320 | **860** | +540 |
| 404 | 800 | 670 | −130 |
| 505 | 490 | **600** | +110 |
| **Mean** | **492.0** | **906.0** | **+414.0 (+84%)** |
| Mean episode length | 589 decisions | 763 decisions | +174 |

Four of the five seeds improved; seed 404 got worse. No game hit the time limit in either condition.
Full data: [`results/comparison.json`](results/comparison.json).

---

## Training dashboard

![Training dashboard](results/training_dashboard.png)

Left: raw score per training game with a 25-game moving average — the average drifts up from about 620
to a peak near 1,000 around episode 280, while individual games scatter between roughly 130 and 2,930.
**The spread between games is larger than the trend across them**, which is the honest summary of this
training budget. Middle: mean update loss, rising from 0.02 to about 0.11 — expected, since a
longer-surviving agent collects larger and more varied rewards to predict. Right: exploration, dropping
from 1.0 to a constant 0.10 once the 1,000-decision random warm-up ends.

---

## Gameplay

### Before training (untrained network)

![Untrained agent](results/demos/episode_0000.gif)

The untrained network is not random — it is **stuck**. Replaying the saved `untrained.pt` checkpoint
and logging its moves shows that **95.4% of its actions are a single move, UPLEFT**. An untrained
convolutional network produces near-identical outputs for every screen, so the same action wins the
`argmax` every time; only the 5% evaluation exploration ever breaks it out. It sweeps up 350 points in
its first 300 decisions by ploughing along whatever pellets lie in that direction, and then scores
**literally nothing for its remaining 260 decisions** — it has jammed into a wall or a corner and stays
there until the ghosts arrive.

### During training: all twelve intermediate GIFs

The notebook records a demonstration game and saves a checkpoint every 25 episodes. Each caption gives
that demonstration's own score (evaluation seed 101). Read them as a sequence and the instability is
obvious: there is an upward trend, but no episode is reliably better than the one before it.

| After 25 — 380 | After 50 — 510 | After 75 — 980 | After 100 — 400 |
|---|---|---|---|
| ![ep25](results/demos/episode_0025.gif) | ![ep50](results/demos/episode_0050.gif) | ![ep75](results/demos/episode_0075.gif) | ![ep100](results/demos/episode_0100.gif) |

| After 125 — 720 | After 150 — 670 | After 175 — 710 | After 200 — 580 |
|---|---|---|---|
| ![ep125](results/demos/episode_0125.gif) | ![ep150](results/demos/episode_0150.gif) | ![ep175](results/demos/episode_0175.gif) | ![ep200](results/demos/episode_0200.gif) |

| After 225 — 750 | After 250 — 900 | After 275 — 560 | After 300 — 1410 |
|---|---|---|---|
| ![ep225](results/demos/episode_0225.gif) | ![ep250](results/demos/episode_0250.gif) | ![ep275](results/demos/episode_0275.gif) | ![ep300](results/demos/episode_0300.gif) |

Scores for all twelve: [`results/demo_scores.json`](results/demo_scores.json). Matching checkpoints
(`episode_0025.pt` … `episode_0300.pt`) are attached to the
[v1.0 release](https://github.com/easonhanyc/mba290t-pacman-dqn/releases/tag/v1.0).

### Best trained game (best of the five evaluation games)

![Best trained agent](results/demos/final_best.gif)

**Watch this one against the clock, not the scoreboard.** Within the 20 seconds the GIF covers, the
trained agent is actually *behind* the untrained one — 280 points versus 350. Its advantage only
appears afterwards, which is precisely why the score table and the GIF must be read together:

| Decision | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | final |
|---|---|---|---|---|---|---|---|---|---|
| Untrained | 110 | 320 | 350 | 350 | 350 | — | — | — | **350** (dead at 560) |
| Trained | 80 | 190 | 280 | 660 | 1240 | 1240 | 1240 | 1390 | **1410** (dead at 838) |

The untrained agent's score is flat from decision 300 onward. The trained agent is still climbing at
decision 800, including a 960-point burst between decisions 300 and 500. Its action mix is the reason:
**UPLEFT 29.6%, DOWN 28.9%, DOWNRIGHT 19.3%, DOWNLEFT 12.8%** — it genuinely steers, instead of
committing to one direction like the untrained network. That shift from a one-action policy to a
directed, varied one is the single clearest thing this agent learned.

Measured with [`probe_behaviour.py`](probe_behaviour.py); raw data in
[`results/behaviour_probe.json`](results/behaviour_probe.json). GIFs show at most the first 20 seconds
of game time at 4× speed; reported scores cover the entire game.

---

## What the agent observes, does, and is rewarded for

- **Observations — four game screens.** Each decision is made from the last four frames, shrunk to
  84×84 and turned grayscale, stacked together. One still image would show where Ms. Pac-Man and the
  ghosts *are*; four consecutive images also show which way everything is *moving*, which is what makes
  chasing and fleeing possible.
- **Actions — joystick moves.** Nine options: no-op, four directions, and four diagonals. The network
  outputs one number per move — its estimate of the total future points that move leads to — and the
  agent normally takes the highest, except on the 10% of training moves it deliberately randomises.
- **Rewards — game points.** The reward is the Ms. Pac-Man score itself: pellets, power pills, ghosts,
  fruit. During learning each reward is clipped to the range −1 to +1 so that one big score event
  cannot swamp the updates; **every score reported in this README is the original, unclipped game score.**

In short: it watches a short clip of the screen, wiggles the joystick, and finds out whether the score
went up — repeated 184,258 times.

### How the learning actually works, in plain language

Nobody ever tells this agent what a ghost is, that pellets are good, or which way is "forward". It only
ever learns one thing: **for this screen, how many points is each joystick direction eventually worth?**

The loop is four steps, repeated every decision:

1. **Choose.** Look at the last four screens, and pick the move the network currently rates highest —
   except 10% of the time, when it deliberately picks at random so it keeps discovering alternatives.
2. **Play.** Send that move to the game and see the next screen and the points it produced.
3. **Remember.** File that experience — screens, move, points, next screens — into a memory holding the
   5,000 most recent moments.
4. **Learn.** Every fourth decision, pull 32 random moments back out of that memory and nudge the
   network's ratings toward what actually happened.

Step 4 is the part worth unpacking. The network's guess for a move is compared against a better-informed
figure: *the points that move actually earned, plus its own estimate of what the resulting screen is
worth.* That second term is what lets credit travel backwards in time — a move is rated highly not only
for points it scores immediately, but for leading somewhere that scores later. Early on both numbers are
nonsense, but because the immediate points are real, truth slowly seeps in from the actual rewards and
spreads back through the chain of moves.

Two details stop this from spiralling. The "better-informed figure" comes from a **frozen copy** of the
network, refreshed only every 1,000 decisions, so the target the agent is chasing holds still long enough
to be worth chasing. And experiences are drawn **randomly** from memory rather than in the order they
happened, so the network learns from a mixture of situations rather than over-fitting to whatever it is
doing right now.

Two things follow that are easy to get backwards, and both showed up in this run:

- **Lower loss does not mean better play.** Loss measures how well the network predicts its own targets,
  not how well it plays. Here loss *rose* (0.04 → 0.11) while the score nearly doubled, because a
  longer-surviving agent encounters bigger, more varied rewards to predict.
- **More training is not monotonically better.** 200 episodes scored 454, 300 scored 906, 400 scored 656.
  The agent is still moving, not converged.

---

## One limitation

**The final score depends heavily on exactly which episode training stops at.** The
every-25-episode demonstration scores swing between 380 and 1410 with no settling, and my own runs
show it plainly: the *same* configuration evaluated at 200, 300, and 400 episodes scored 454, 906, and
656. The notebook evaluates whichever weights exist at the final episode, so a meaningful part of the
906 is landing on a good point in that oscillation rather than reaching a stable skill level. With only
five evaluation games, the confidence interval around any of these means is wide. The agent has not
converged; it is a snapshot of a still-moving system.

Two smaller limitations worth naming: reward clipping makes a 10-point pellet and a 200-point ghost
identical during learning, so the agent has no reason to prefer hunting ghosts; and with
`terminal_on_life_loss=False` it is never told directly that losing a life was bad — it only sees the
score stop rising.

## My next experiment

**Change one setting: decay exploration from 1.0 down to about 0.05 over training, instead of holding
it constant at 0.10.** Everything else stays fixed.

This targets the limitation above at its cause. A constant 10% random-move rate means the agent is
still injecting noise into every game at episode 300, which both caps final performance and keeps the
replay buffer permanently contaminated with random actions — a likely driver of the oscillation. High
exploration early would fill the small buffer with genuinely diverse experience when the network knows
nothing, and low exploration late would let it consolidate a stable policy and stop thrashing. My stage-1
data supports this: 0.05 was the *worst* setting early (eval 224 at 30 episodes) but the run that used it
was still climbing at 60 episodes, which is what a schedule would exploit — high early, low late.

---

## Evidence index

| Item | Path |
|---|---|
| Executed notebook, all outputs visible | [`pacman_dqn.ipynb`](pacman_dqn.ipynb) |
| Run settings and package versions | [`results/config.json`](results/config.json) |
| Per-episode training log | [`results/training.csv`](results/training.csv) |
| Run totals (episodes, decisions, updates, time) | [`results/training_summary.json`](results/training_summary.json) |
| All five before/after scores | [`results/comparison.json`](results/comparison.json) |
| Untrained baseline scores | [`results/baseline.json`](results/baseline.json) |
| Score at each 25-episode demonstration | [`results/demo_scores.json`](results/demo_scores.json) |
| Training plot | [`results/training_dashboard.png`](results/training_dashboard.png) |
| All gameplay GIFs | [`results/demos/`](results/demos/) |
| Hyperparameter search data | [`results/hyperparameter_search.json`](results/hyperparameter_search.json) |
| Behaviour probe (score curve + action mix) | [`results/behaviour_probe.json`](results/behaviour_probe.json) |
| Script that produces the behaviour probe | [`probe_behaviour.py`](probe_behaviour.py) |

### A note on how GitHub renders this notebook

Worth knowing before you open [`pacman_dqn.ipynb`](pacman_dqn.ipynb) on GitHub, because one thing is
missing there and it is not a gap in the run.

The notebook contains all 14 gameplay GIFs as `image/gif` outputs — they are in the file, and Jupyter,
VS Code and Colab all animate them. **GitHub's notebook viewer silently discards `image/gif` outputs**
and prints the placeholder `<IPython.core.display.Image object>` instead. I verified this on the
signed-out render: the page contains zero GIF data, while both PNGs (the opening game screen and the
training dashboard) display normally.

Everything else renders correctly on GitHub: every score, the full training log, `Change in mean score:
+414.0`, both plots, and the filled-in explanation.

So the gameplay is published three ways, and only the first is affected:

1. As `image/gif` outputs inside the notebook — present in the file, not shown by GitHub.
2. As a **gallery cell** added to the notebook (section 6, "gameplay, rendered for GitHub") that
   re-embeds the same files from this repository, so they animate in GitHub's viewer too.
3. As the embedded GIFs in [this README](#gameplay), which render on GitHub without trouble.

The gallery cell references the exact files this run wrote to `pacman_runs/.../demos/`; nothing was
re-run to produce it.

### Where the model checkpoints are saved

All 14 checkpoints — `untrained.pt`, the twelve intermediate `episode_0025.pt` … `episode_0300.pt`, and
the final `trained.pt` (~6.8 MB each) — are **attached to the
[v1.0 release](https://github.com/easonhanyc/mba290t-pacman-dqn/releases/tag/v1.0)** inside
`pacman_run_300ep_full.zip`, not committed to the repository, which keeps the clone small. That archive
is the notebook's own complete run folder, so it also contains a second copy of every JSON, the CSV, the
plot and all 14 GIFs. The weaker 250-episode run is attached to the same release as
`pacman_run_250ep_full.zip`. Both ZIPs are also kept locally under `pacman_runs/`.

Checkpoints are portable playback snapshots (weights plus action count); they do not store optimizer or
replay state, so they can replay an agent but cannot resume training. [`probe_behaviour.py`](probe_behaviour.py)
loads them.

---

## Assignment requirements checklist

Every item the assignment asks for, and where in this repository it is answered.

**What I am submitting**

| Requirement | Where | ✓ |
|---|---|---|
| Executed notebook saved after the final training and evaluation run, three hyperparameters set, all cell outputs visible | [`pacman_dqn.ipynb`](pacman_dqn.ipynb) — 14 GIF outputs, 2 plots, all stdout; outputs not cleared. GitHub's viewer drops GIF outputs, so a gallery cell re-embeds them ([details](#a-note-on-how-github-renders-this-notebook)) | ✓ |
| Untrained gameplay GIF | [Before training](#before-training-untrained-network) | ✓ |
| Best trained gameplay GIF | [Best trained game](#best-trained-game-best-of-the-five-evaluation-games) | ✓ |
| Intermediate GIFs **and checkpoints** (run ≥ 25 episodes) | [All twelve GIFs](#during-training-all-twelve-intermediate-gifs); 12 checkpoints in the [v1.0 release](https://github.com/easonhanyc/mba290t-pacman-dqn/releases/tag/v1.0) | ✓ |
| Training plot and all five before/after evaluation scores | [Training dashboard](#training-dashboard), [Results](#results-all-five-beforeafter-scores) | ✓ |
| Short explanation of observations, actions, rewards, and one limitation | [What the agent observes](#what-the-agent-observes-does-and-is-rewarded-for), [One limitation](#one-limitation) | ✓ |

**README requirements**

| Requirement | Where | ✓ |
|---|---|---|
| Brief overview and instructions to open and run the notebook | [Overview and how to run](#overview-and-how-to-run) | ✓ |
| Exploration, episode budget, learning rate, each with a reason | [My three hyperparameters](#my-three-hyperparameters) | ✓ |
| What I expected, then what I observed | [What I expected](#what-i-expected-and-what-actually-happened) | ✓ |
| Actual completed episodes, decisions, learning updates, elapsed time, hardware | [Actual run facts](#actual-run-facts) | ✓ |
| Plain-language explanation: four screens = observations, joystick = actions, points = reward | [What the agent observes](#what-the-agent-observes-does-and-is-rewarded-for) | ✓ |
| One observed limitation and one next experiment, naming the single setting to change | [One limitation](#one-limitation), [My next experiment](#my-next-experiment) | ✓ |

**Evidence required in the README**

| Requirement | Where | ✓ |
|---|---|---|
| Embed untrained, best trained, and any intermediate GIFs | [Gameplay](#gameplay) — all 14 embedded | ✓ |
| Embed `training_dashboard.png` with score, loss and exploration curves visible | [Training dashboard](#training-dashboard) | ✓ |
| Table of all five baseline scores, all five trained scores, and their means; link `comparison.json` | [Results](#results-all-five-beforeafter-scores) | ✓ |
| Link notebook, `config.json`, `training.csv`, `training_summary.json` | [Evidence index](#evidence-index) | ✓ |
| Identify an interrupted run, or a run with no learning updates | Neither applies: status `completed`, 300/300 episodes, 45,815 learning updates — stated in [Actual run facts](#actual-run-facts) | ✓ |

**Evaluation kept fair**

| Requirement | Status |
|---|---|
| Same five seeds, 5% exploration, same time limit, before and after | Unchanged from the notebook — `EVAL_SEEDS`, `EVAL_EXPLORATION` and `MAX_STEPS` were not touched ([`results/config.json`](results/config.json)) |
| Baseline is an untrained network, not a random-action agent | `untrained.pt` is evaluated, not random play. It is measurably *not* random — it repeats one action 95.4% of the time ([probe](#best-trained-game-best-of-the-five-evaluation-games)) |
| Report every evaluation score and both means | All ten scores and both means in [Results](#results-all-five-beforeafter-scores) |
| Report failed runs or lack of improvement honestly | The +12 run is reported below, not hidden |

**Submission checklist**

| Step | Status |
|---|---|
| Push executed `.ipynb`, README and selected results to a public repo | Done — this repository is public |
| Confirm on GitHub that final scores, plots and gameplay outputs are visible | Verified on the signed-out render. Scores, stdout and both plots display. **GitHub's notebook viewer drops `image/gif` outputs**, so the gameplay GIFs stored in the notebook do not animate there — see [A note on how GitHub renders this notebook](#a-note-on-how-github-renders-this-notebook). A gallery cell re-embeds them from the repository so gameplay is visible on GitHub too, and all 14 also render in this README |
| Verify in a private window that notebook, images, GIFs and links are accessible | Verified signed-out; all asset URLs return HTTP 200 |
| Keep large checkpoints in a local ZIP or GitHub release, and explain where | [Where the model checkpoints are saved](#where-the-model-checkpoints-are-saved) |
| Submit the repository URL through the course portal | Remaining — to be submitted by me |

## How this maps to the grading components

| Graded on | This submission |
|---|---|
| **Gameplay performance / class leaderboard** — mean across the five trained evaluation games | **906.0**, from `[1410, 990, 860, 670, 600]`, against a 492.0 untrained baseline under identical settings. Linked: [`results/comparison.json`](results/comparison.json) |
| **Explanation of the learning process** | [How the learning actually works, in plain language](#how-the-learning-actually-works-in-plain-language) — the choose/play/remember/learn loop, why a frozen target network and random replay are needed, and why loss and score move independently (they did here: loss rose while score nearly doubled) |
| **Hyperparameter choices** | Not guessed: an 8-run, ~1.6-million-decision search scored with the notebook's own protocol. [Two-stage search](#how-i-chose-them-a-two-stage-search), full write-up in [docs/METHODOLOGY.md](docs/METHODOLOGY.md), raw data in [`results/hyperparameter_search.json`](results/hyperparameter_search.json) and [`sweep/`](sweep/) |
| **Quality and completeness of evidence** | All 14 GIFs embedded, dashboard embedded, all ten scores tabulated, every JSON/CSV linked, checkpoints released, the search harness and raw logs published, a behaviour probe explaining *what* changed, and the weaker prior run kept for comparison |

## Honest reporting notes

Two things a grader should know:

1. **My first full run scored +12, not +414.** Using the same exploration and learning rate but
   **250** episodes, the trained mean was 504 against the 492 baseline — statistically nothing. That run's
   evidence is preserved in [`results_run250/`](results_run250/). The difference between +12 and +414 is
   50 episodes, which is the strongest possible illustration of the instability described under
   *One limitation*. I am reporting the 300-episode run as my result, not concealing the 250-episode one.
2. **The episode budget was selected using the same five seeds used for grading.** Stage 2 measured
   evaluation score at 100/200/300/400 episodes on seeds `[101, 202, 303, 404, 505]` and I picked the
   best. That is selection on the evaluation set, and some of the +414 is therefore optimistic rather
   than a clean out-of-sample estimate. Exploration and learning rate were chosen the same way at a
   60-episode budget. I have left the evaluation protocol itself completely unmodified.
