---
title: Deep Q-Network
type: concept
summary: A Deep Q-Network (DQN) is a reinforcement-learning method in which a neural network estimates how much future reward each possible action is worth, and the agent takes the highest-valued move.
sources:
- path: raw/course-projects/pacman-dqn/README.md
  source_id: course-projects-pacman-dqn-readme-4b724349
  sha256: 4b724349cd4ac689449f79321b89b5b06e31ce2de3031633fa290309ae100401
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:58:38'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Deep Q-Network

A Deep Q-Network (DQN) is a reinforcement-learning method in which a neural network estimates how much future reward each possible action is worth, and the agent takes the highest-valued move. In these sources it is the algorithm behind the Ms. Pac-Man agent: a convolutional network reads stacked game screens and a slower-moving target network supplies the learning target.

## Key facts
- The agent observes four game screens, which are shrunk to 84x84 and turned grayscale and stacked together for decision-making. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])
- The agent has nine possible actions: no-op, four directions, and four diagonals. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])
- The reward used for learning is the Ms. Pac-Man score, which is clipped to the range of -1 to +1 during learning. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])
- The agent learns by comparing the network's guess for a move against the actual points earned plus an estimate of the resulting screen's worth, allowing credit to travel backward in time. ([[raw/course-projects/pacman-dqn/README#How the learning actually works, in plain language|course-projects/pacman-dqn/README.md › How the learning actually works, in plain language]])

## Related notes
- [[Ms. Pac-Man DQN]] — The project that applies this method, with its chosen settings and results.
- [[Deep Learning]] — The Q-network is a convolutional neural network trained on the game screens.

## Sources
- [[raw/course-projects/pacman-dqn/README|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Ms. Pac-Man DQN — Class 3 Assignment]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/README.md)
