---
title: Deep Q-Network
type: concept
summary: A Deep Q-Network was trained to play Ms.
sources:
- path: raw/course-projects/pacman-dqn/README.md
  source_id: course-projects-pacman-dqn-readme-4b724349
  sha256: 4b724349cd4ac689449f79321b89b5b06e31ce2de3031633fa290309ae100401
- path: raw/website/projects/pacman-dqn.md
  source_id: website-projects-pacman-dqn-6c3cd8ae
  sha256: 6c3cd8aecdb8a7c7eeceb74b748cdf8a40c1470a571d362d705990531de00d4c
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Deep Q-Network

A Deep Q-Network was trained to play Ms. Pac-Man, resulting in a mean evaluation score increase from 492 to 906. The project also revealed that the untrained baseline was not random but was stuck repeating a single move.

## Key facts

### From course-projects/pacman-dqn/README.md
- Training a Deep Q-Network to play Ms. Pac-Man was done using the course notebook pacman_dqn.ipynb. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The student-chosen settings for the training were exploration = 0.10, episodes = 300, and learning rate = 0.0001. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The headline result showed the mean evaluation score rose from 492 (untrained) to 906 (trained), representing a +414 / +84% increase. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The untrained network is not random, but is stuck, with 95.4% of its actions being a single move, UPLEFT. ([[raw/course-projects/pacman-dqn/README#Before training (untrained network)|course-projects/pacman-dqn/README.md › Before training (untrained network)]])
- An untrained convolutional network produces near-identical outputs for every screen, causing the same action to win the argmax every time. ([[raw/course-projects/pacman-dqn/README#Before training (untrained network)|course-projects/pacman-dqn/README.md › Before training (untrained network)]])

### From website/projects/pacman-dqn.md
- The comparison between baseline and trained scores was made using identical evaluation settings to ensure a like-for-like comparison. ([[raw/website/projects/pacman-dqn|website/projects/pacman-dqn.md]])
- The mean evaluation score rose from 492 to 906, which is an 84% increase. ([[raw/website/projects/pacman-dqn|website/projects/pacman-dqn.md › front matter]])
- The untrained baseline was not random; it was stuck repeating one move 95.4% of the time. ([[raw/website/projects/pacman-dqn|website/projects/pacman-dqn.md › front matter]])

## Related notes
- [[Ms. Pac-Man DQN Implementation]] — Ms. Pac-Man DQN Implementation: The core algorithm used to train the agent.
- [[Pac-Man DQN Methodology Study]] — Pac-Man DQN Methodology Study: The core reinforcement learning algorithm used for the agent.

## Sources
- [[raw/course-projects/pacman-dqn/README|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Ms. Pac-Man DQN — Class 3 Assignment]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/README.md)
- [[raw/website/projects/pacman-dqn|Personal website - projects: Ms. Pac-Man DQN]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/pacman-dqn.md)
