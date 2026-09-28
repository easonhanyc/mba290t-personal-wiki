---
title: Pac-Man DQN Methodology Study
type: project
summary: This document details the methodology used to select and test hyperparameters for a Pac-Man DQN agent.
sources:
- path: raw/course-projects/pacman-dqn/docs/METHODOLOGY.md
  source_id: course-projects-pacman-dqn-docs-methodology-b14e34e7
  sha256: b14e34e7414beca5cf07a7ff1ef0d2e01a831cc2ee11613cc29ba7a5a7fb6290
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Pac-Man DQN Methodology Study

This document details the methodology used to select and test hyperparameters for a Pac-Man DQN agent. It records the hardware, measurement protocols, and findings from various training stages, highlighting the impact of replay buffer size and learning rate.

## Key facts
- The three values in the notebook were not guessed. They came from 8 training runs totalling roughly 1.6 million agent decisions, scored with the notebook's own evaluation protocol. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY|course-projects/pacman-dqn/docs/METHODOLOGY.md › Methodology: how the three settings were chosen]])
- The replay buffer holds only 5,000 transitions — about seven games. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The problem with guessing|course-projects/pacman-dqn/docs/METHODOLOGY.md › The problem with guessing]])
- The target network sync only every 1,000 decisions. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The problem with guessing|course-projects/pacman-dqn/docs/METHODOLOGY.md › The problem with guessing]])
- The harness extracts the notebook's logic cell-for-cell — make_env, DQN, ReplayMemory, choose_action, learn, and evaluate, plus every fixed constant. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The harness|course-projects/pacman-dqn/docs/METHODOLOGY.md › The harness]])
- Apple M2, 8 cores, 16 GB RAM, macOS 26.6.2 arm64, Python 3.12.14, PyTorch 2.14.0. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Hardware and measured throughput|course-projects/pacman-dqn/docs/METHODOLOGY.md › Hardware and measured throughput]])
- MPS is ~2.7× faster than CPU for this network, so a 300-episode run costs about 19 minutes rather than the hour a CPU estimate suggests. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Hardware and measured throughput|course-projects/pacman-dqn/docs/METHODOLOGY.md › Hardware and measured throughput]])
- Every learning rate above 1e-4 was worse, monotonically, at the 60-episode mark. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY|course-projects/pacman-dqn/docs/METHODOLOGY.md › Stage 1 — exploration × learning rate]])
- Exploration of 0.05 produced the worst agent in the whole study (224 at 30 episodes). ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY|course-projects/pacman-dqn/docs/METHODOLOGY.md › Stage 1 — exploration × learning rate]])
- The larger buffer was worse at three of the four checkpoints when comparing 5,000 transitions to 50,000 transitions. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY|course-projects/pacman-dqn/docs/METHODOLOGY.md › Stage 2 — episode budget, and one test of a "fixed" setting]])
- Episode count is strongly non-monotonic — 454 → 906 → 656 across 200/300/400 episodes. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY|course-projects/pacman-dqn/docs/METHODOLOGY.md › Stage 2 — episode budget, and one test of a "fixed" setting]])
- The untrained network is not random — it is stuck. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Behaviour probe|course-projects/pacman-dqn/docs/METHODOLOGY.md › Behaviour probe]])
- What training bought, most visibly, is the ability to steer. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Behaviour probe|course-projects/pacman-dqn/docs/METHODOLOGY.md › Behaviour probe]])

## Related notes
- [[Ms. Pac-Man DQN Implementation]] — This note details the implementation of the DQN agent, while this note details the methodology used to tune it.
- [[From Zero to AI Agents]] — This course provides the foundational knowledge for building and evaluating AI agents like the one studied here.
- [[Deep Q-Network]] — The core reinforcement learning algorithm used for the agent.

## Sources
- [[raw/course-projects/pacman-dqn/docs/METHODOLOGY|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Methodology: how the three settings were chosen]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/docs/METHODOLOGY.md)
