---
title: "Ms. Pac-Man DQN"
description: "A Deep Q-Network that nearly doubled its score — and a baseline that turned out to be measuring the wrong thing."
summary: "Mean evaluation score rose from 492 to 906 (+84%). The more interesting finding was that the untrained baseline wasn't random at all — it was stuck, repeating one move 95.4% of the time, which means the headline number flatters the result."
role: "MBA 290T — Fundamentals of Agentic AI"
period: "Sep 2026"
depth: "project"
org: "UC Berkeley"
badges: ["Reinforcement learning"]
live: false
tags: ["ai"]
metrics:
  - n: "+84%"
    l: "906 vs 492 baseline"
  - n: "8"
    l: "search runs"
  - n: "1.6M"
    l: "agent decisions searched"
  - n: "95.4%"
    l: "of baseline moves were one action"
links:
  code: "https://github.com/easonhanyc/mba290t-pacman-dqn"
featured: false
order: 8
---

**Measurement:** baseline and trained scores come from identical evaluation settings, so the comparison is like-for-like

> **The 30-second version.** I trained a Deep Q-Network on Ms. Pac-Man and nearly doubled its score. But the finding I'd actually defend in a room is that the *baseline* was measuring the wrong thing — and that three of my going-in assumptions turned out to be wrong in ways the data made unambiguous.

---

## 1. The headline number, and why it flatters

Mean score across five fixed evaluation seeds rose from **492 to 906**. Four of five seeds improved; one got worse.

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 250" role="img" aria-labelledby="pm-t" xmlns="http://www.w3.org/2000/svg">
<title id="pm-t">Mean evaluation score rose from 492 to 906, but the untrained baseline was not random: it repeated a single action 95.4 per cent of the time</title>
<g font-family="var(--mono)" font-size="10.5">
<text x="0" y="12" fill="var(--ink-3)" letter-spacing="1.2">MEAN EVALUATION SCORE</text>
<rect x="0" y="26" width="150" height="34" rx="3" fill="var(--ink)" opacity="0.16"/>
<rect x="0" y="70" width="276" height="34" rx="3" fill="var(--accent)"/>
<text x="160" y="48" fill="var(--ink-2)">492 · untrained</text>
<text x="286" y="92" fill="var(--ink-2)">906 · trained &#183; +84%</text>
<line x1="0" y1="132" x2="700" y2="132" stroke="var(--border-strong)"/>
<text x="0" y="158" fill="var(--ink-3)" letter-spacing="1.2">WHAT THE UNTRAINED BASELINE ACTUALLY DID</text>
<rect x="0" y="172" width="620" height="30" rx="3" fill="var(--gold)" opacity="0.85"/>
<rect x="622" y="172" width="78" height="30" rx="3" fill="var(--ink)" opacity="0.16"/>
<text x="12" y="192" fill="#1a1a1a" font-weight="500">ONE SINGLE ACTION, REPEATED — 95.4%</text>
<text x="0" y="224" fill="var(--ink-2)">Not a random agent. A stuck one — so the gain is measured against a floor that barely plays.</text>
</g>
</svg>
</div>
<figcaption>Figures as reported in the write-up below.</figcaption>
</figure>

Then I replayed the untrained checkpoint and logged what it was actually doing. **95.4% of its moves were a single action — UPLEFT.**

An untrained convolutional network scores every screen almost identically, so the same action wins the `argmax` every time. The "baseline" agent ploughs along whatever pellets lie in one direction, banks 350 points in its first 300 decisions, then scores *literally nothing* for its remaining 260 — jammed in a corner until the ghosts arrive.

> So a large share of that +414 is the agent learning to **steer at all**. The 492-point baseline flatters something that is really just walking into a wall. The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%), and that shift — from a one-action policy to a directed one — is the clearest thing it actually learned.

Reporting +84% without that caveat would be technically true and substantively misleading.

## 2. Three things I expected that were wrong

**I expected a bigger replay buffer to be the single largest available win.** The stock buffer holds 5,000 transitions, which seemed obviously too small. I tested one 10× larger. It was **worse at three of four checkpoints**. So I left every fixed classroom setting untouched and changed only the three permitted values. The obvious hypothesis was wrong and the measurement was worth taking.

**I expected improvement to be smooth.** It is violently non-monotonic. The same configuration evaluated at 200, 300 and 400 episodes scored **454, 906, 656**. Per-25-episode demonstrations ran 380, 510, 980, 400, 720, 670, 710, 580, 750, 900, 560, 1410. There is an upward trend, but any individual checkpoint is a lottery — stopping at episode 275 instead of 300 would have produced a much weaker agent.

**I expected falling loss to mean better play.** Loss *rose*, from 0.040 to 0.110, while the score nearly doubled. That is healthy: as the agent survives longer it collects larger and more varied rewards to predict. Loss measures prediction of its own moving targets, not skill. It is not a scoreboard.

## 3. How the settings were chosen

Not by guessing. I extracted the notebook's exact training and evaluation logic into a standalone harness and searched — 8 runs, roughly 1.6 million agent decisions — scoring every configuration with the notebook's own protocol (same five seeds, same exploration, same time limit) so the numbers stayed comparable.

| Setting | Chosen | Why |
|---|---|---|
| Exploration | `0.10` | At `0.05` the agent collapsed into a stuck policy (eval 224) because a small replay buffer fills with near-identical states. At `0.20` a fifth of all moves are noise. |
| Episodes | `300` | Where measured score peaked, within the compute I had (≈19 min). |
| Learning rate | `0.0001` | Every increase made learning *worse*: 0.00025 → 288 and 0.0005 → 320 at 60 episodes, against 1030 for 0.0001. |

One result from the search is worth keeping: at 30 episodes, *every* configuration sat at or below the untrained baseline. A short run is genuinely worse than no training at all — the network has moved away from its accidentally-reasonable random initialisation without having learned anything yet.

## 4. What I'd want a reviewer to know

**My first full run scored +12, not +414.** Same exploration and learning rate, 250 episodes instead of 300: trained mean 504 against a 492 baseline — statistically nothing. That run's evidence is preserved in the repository rather than deleted. The difference between +12 and +414 is fifty episodes, which is the strongest illustration of the instability above.

**The episode budget was selected using the same five seeds used for grading.** I measured score at 100/200/300/400 episodes on the evaluation seeds and picked the best. That is selection on the evaluation set, so part of the +414 is optimistic rather than a clean out-of-sample estimate. The evaluation protocol itself I left completely unmodified.

**The agent has not converged.** It is a snapshot of a still-moving system, and with five evaluation games the confidence interval around any of these means is wide.

## 5. The next experiment

Change one setting: **decay exploration from 1.0 to about 0.05 across training**, instead of holding it at a constant 0.10.

This targets the instability at its cause. A constant 10% random-move rate means the agent is still injecting noise at episode 300, which both caps final performance and keeps the small replay buffer permanently contaminated with random actions. High exploration early would fill it with diverse experience while the network knows nothing; low exploration late would let it consolidate instead of thrashing. The stage-1 data supports it: `0.05` was the *worst* setting early but was still climbing at 60 episodes — exactly what a schedule would exploit.
