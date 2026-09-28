---
title: Ms. Pac-Man DQN Implementation
type: project
summary: This project details the implementation of a Deep Q-Network (DQN) agent trained to play Ms.
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

# Ms. Pac-Man DQN Implementation

This project details the implementation of a Deep Q-Network (DQN) agent trained to play Ms. Pac-Man. The agent learned to improve its performance significantly, with the mean evaluation score rising from 492 to 906 after training.

## Key facts

### From course-projects/pacman-dqn/README.md
- The three student-chosen settings were exploration = 0.10, episodes = 300, learning rate = 0.0001. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The headline result showed the mean evaluation score rose from 492 (untrained) to 906 (trained), which is a +414 / +84% increase. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The agent sees four stacked 84×84 grayscale game screens, picks one of nine joystick actions, and learns from the game's own score. ([[raw/course-projects/pacman-dqn/README#Overview and how to run|course-projects/pacman-dqn/README.md › Overview and how to run]])
- The mean evaluation score before training was 492.0 and after training it was 906.0. ([[raw/course-projects/pacman-dqn/README|course-projects/pacman-dqn/README.md › Results: all five before/after scores]])
- The exploration setting of 0.10 was chosen because at 0.05 the agent collapsed into a degenerate, stuck policy. ([[raw/course-projects/pacman-dqn/README#My three hyperparameters|course-projects/pacman-dqn/README.md › My three hyperparameters]])
- The learning rate of 0.0001 was chosen because every increase made learning worse, not faster. ([[raw/course-projects/pacman-dqn/README#My three hyperparameters|course-projects/pacman-dqn/README.md › My three hyperparameters]])
- The mean update loss went from 0.040 (first 25 episodes) to 0.110 (last 25). ([[raw/course-projects/pacman-dqn/README#What I expected, and what actually happened|course-projects/pacman-dqn/README.md › What I expected, and what actually happened]])
- The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%) compared to the untrained baseline's 95.4% UPLEFT. ([[raw/course-projects/pacman-dqn/README#What I expected, and what actually happened|course-projects/pacman-dqn/README.md › What I expected, and what actually happened]])
- The untrained network is stuck, with 95.4% of its actions being a single move, UPLEFT. ([[raw/course-projects/pacman-dqn/README#Before training (untrained network)|course-projects/pacman-dqn/README.md › Before training (untrained network)]])
- The trained agent's action mix was UPLEFT 29.6%, DOWN 28.9%, DOWNRIGHT 19.3%, and DOWNLEFT 12.8%. ([[raw/course-projects/pacman-dqn/README#Best trained game (best of the five evaluation games)|course-projects/pacman-dqn/README.md › Best trained game (best of the five evaluation games)]])
- Observations consist of four game screens, shrunk to 84x84 and turned grayscale, stacked together. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])
- The reward is the Ms. Pac-Man score itself, which is clipped to the range -1 to +1 during learning. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])

### From website/projects/pacman-dqn.md
- Mean score across five fixed evaluation seeds rose from 492 to 906. ([[raw/website/projects/pacman-dqn#1. The headline number, and why it flatters|website/projects/pacman-dqn.md › 1. The headline number, and why it flatters]])
- 95.4% of its moves were a single action — UPLEFT. ([[raw/website/projects/pacman-dqn#1. The headline number, and why it flatters|website/projects/pacman-dqn.md › 1. The headline number, and why it flatters]])
- The trained agent's moves spread across four directions (29.6 / 28.9 / 19.3 / 12.8%). ([[raw/website/projects/pacman-dqn#1. The headline number, and why it flatters|website/projects/pacman-dqn.md › 1. The headline number, and why it flatters]])
- I expected a bigger replay buffer to be the single largest available win. ([[raw/website/projects/pacman-dqn#2. Three things I expected that were wrong|website/projects/pacman-dqn.md › 2. Three things I expected that were wrong]])
- It is violently non-monotonic. ([[raw/website/projects/pacman-dqn#2. Three things I expected that were wrong|website/projects/pacman-dqn.md › 2. Three things I expected that were wrong]])
- Loss rose, from 0.040 to 0.110, while the score nearly doubled. ([[raw/website/projects/pacman-dqn#2. Three things I expected that were wrong|website/projects/pacman-dqn.md › 2. Three things I expected that were wrong]])
- I extracted the notebook's exact training and evaluation logic into a standalone harness and searched — 8 runs, roughly 1.6 million agent decisions. ([[raw/website/projects/pacman-dqn#3. How the settings were chosen|website/projects/pacman-dqn.md › 3. How the settings were chosen]])
- At 30 episodes, every configuration sat at or below the untrained baseline. ([[raw/website/projects/pacman-dqn#3. How the settings were chosen|website/projects/pacman-dqn.md › 3. How the settings were chosen]])
- My first full run scored +12, not +414. ([[raw/website/projects/pacman-dqn#4. What I'd want a reviewer to know|website/projects/pacman-dqn.md › 4. What I'd want a reviewer to know]])
- The episode budget was selected using the same five seeds used for grading. ([[raw/website/projects/pacman-dqn#4. What I'd want a reviewer to know|website/projects/pacman-dqn.md › 4. What I'd want a reviewer to know]])
- Change one setting: decay exploration from 1.0 to about 0.05 across training, instead of holding it at a constant 0.10. ([[raw/website/projects/pacman-dqn#5. The next experiment|website/projects/pacman-dqn.md › 5. The next experiment]])

## Related notes
- [[From Zero to AI Agents]] — This project is an application of the concepts taught in the From Zero to AI Agents course.
- [[Pac-Man DQN Methodology Study]] — This source details the methodology used to select and test hyperparameters for a Pac-Man DQN agent.
- [[Deep Learning]] — The core reinforcement learning technique used to train the agent.
- [[Deep Q-Network]] — The core algorithm used to train the agent.

## Sources
- [[raw/course-projects/pacman-dqn/README|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Ms. Pac-Man DQN — Class 3 Assignment]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/README.md)
- [[raw/website/projects/pacman-dqn|Personal website - projects: Ms. Pac-Man DQN]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/pacman-dqn.md)
