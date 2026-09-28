---
title: Ms. Pac-Man DQN
type: project
summary: 'Ms. Pac-Man DQN was the MBA 290T Class 3 assignment: a Deep Q-Network trained to play Ms. Pac-Man, with exploration 0.10, 300 episodes and learning rate 0.0001 chosen by a measured search.'
sources:
- path: raw/course-projects/pacman-dqn/README.md
  source_id: course-projects-pacman-dqn-readme-4b724349
  sha256: 4b724349cd4ac689449f79321b89b5b06e31ce2de3031633fa290309ae100401
- path: raw/website/projects/pacman-dqn.md
  source_id: website-projects-pacman-dqn-6c3cd8ae
  sha256: 6c3cd8aecdb8a7c7eeceb74b748cdf8a40c1470a571d362d705990531de00d4c
- path: raw/course-projects/pacman-dqn/docs/METHODOLOGY.md
  source_id: course-projects-pacman-dqn-docs-methodology-b14e34e7
  sha256: b14e34e7414beca5cf07a7ff1ef0d2e01a831cc2ee11613cc29ba7a5a7fb6290
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Ms. Pac-Man DQN

Ms. Pac-Man DQN was the MBA 290T Class 3 assignment: a Deep Q-Network trained to play Ms. Pac-Man, with exploration 0.10, 300 episodes and learning rate 0.0001 chosen by a measured search. Its mean evaluation score rose from 492 to 906 (+84%), but the untrained baseline was stuck repeating one move 95.4% of the time, so the headline number flatters the result.

## Key facts

### From course-projects/pacman-dqn/README.md
- The three student-chosen settings were exploration = 0.10, episodes = 300, learning rate = 0.0001. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The headline result showed the mean evaluation score rose from 492 (untrained) to 906 (trained), which is a +414 / +84% increase. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The agent sees four stacked 84×84 grayscale game screens, picks one of nine joystick actions, and learns from the game's own score. ([[raw/course-projects/pacman-dqn/README#Overview and how to run|course-projects/pacman-dqn/README.md › Overview and how to run]])
- The exploration setting of 0.10 was chosen because at 0.05 the agent collapsed into a degenerate, stuck policy. ([[raw/course-projects/pacman-dqn/README#My three hyperparameters|course-projects/pacman-dqn/README.md › My three hyperparameters]])
- The learning rate of 0.0001 was chosen because every increase made learning worse, not faster. ([[raw/course-projects/pacman-dqn/README#My three hyperparameters|course-projects/pacman-dqn/README.md › My three hyperparameters]])
- The mean update loss went from 0.040 (first 25 episodes) to 0.110 (last 25). ([[raw/course-projects/pacman-dqn/README#What I expected, and what actually happened|course-projects/pacman-dqn/README.md › What I expected, and what actually happened]])
- The untrained network is stuck, with 95.4% of its actions being a single move, UPLEFT. ([[raw/course-projects/pacman-dqn/README#Before training (untrained network)|course-projects/pacman-dqn/README.md › Before training (untrained network)]])
- The trained agent's action mix was UPLEFT 29.6%, DOWN 28.9%, DOWNRIGHT 19.3%, and DOWNLEFT 12.8%. ([[raw/course-projects/pacman-dqn/README#Best trained game (best of the five evaluation games)|course-projects/pacman-dqn/README.md › Best trained game (best of the five evaluation games)]])
- The reward is the Ms. Pac-Man score itself, which is clipped to the range -1 to +1 during learning. ([[raw/course-projects/pacman-dqn/README#What the agent observes, does, and is rewarded for|course-projects/pacman-dqn/README.md › What the agent observes, does, and is rewarded for]])

### From website/projects/pacman-dqn.md
- The 492 → 906 means are over five fixed evaluation seeds; four of the five seeds improved and one got worse. ([[raw/website/projects/pacman-dqn#1. The headline number, and why it flatters|website/projects/pacman-dqn.md › 1. The headline number, and why it flatters]])
- A bigger replay buffer was expected to be the largest available win; in the search the 10× larger buffer (50,000 transitions) was worse at three of the four checkpoints. ([[raw/website/projects/pacman-dqn#2. Three things I expected that were wrong|website/projects/pacman-dqn.md › 2. Three things I expected that were wrong]])
- Improvement was violently non-monotonic: the same configuration scored 454, 906 and 656 at 200, 300 and 400 episodes. ([[raw/website/projects/pacman-dqn#2. Three things I expected that were wrong|website/projects/pacman-dqn.md › 2. Three things I expected that were wrong]])
- The settings came from a standalone harness that replicates the notebook's training and evaluation logic: 8 runs, roughly 1.6 million agent decisions. ([[raw/website/projects/pacman-dqn#3. How the settings were chosen|website/projects/pacman-dqn.md › 3. How the settings were chosen]])
- At 30 episodes, every configuration sat at or below the untrained baseline. ([[raw/website/projects/pacman-dqn#3. How the settings were chosen|website/projects/pacman-dqn.md › 3. How the settings were chosen]])
- The first full run (250 episodes instead of 300) scored +12 over the baseline, not +414. ([[raw/website/projects/pacman-dqn#4. What I'd want a reviewer to know|website/projects/pacman-dqn.md › 4. What I'd want a reviewer to know]])
- The episode budget was selected using the same five seeds used for grading. ([[raw/website/projects/pacman-dqn#4. What I'd want a reviewer to know|website/projects/pacman-dqn.md › 4. What I'd want a reviewer to know]])
- Proposed next experiment: decay exploration from 1.0 to about 0.05 across training instead of holding it at a constant 0.10. ([[raw/website/projects/pacman-dqn#5. The next experiment|website/projects/pacman-dqn.md › 5. The next experiment]])

### From course-projects/pacman-dqn/docs/METHODOLOGY.md
- The replay buffer holds only 5,000 transitions — about seven games. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The problem with guessing|course-projects/pacman-dqn/docs/METHODOLOGY.md › The problem with guessing]])
- The target network syncs only every 1,000 decisions. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The problem with guessing|course-projects/pacman-dqn/docs/METHODOLOGY.md › The problem with guessing]])
- The harness extracts the notebook's logic cell-for-cell — make_env, DQN, ReplayMemory, choose_action, learn, and evaluate, plus every fixed constant. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#The harness|course-projects/pacman-dqn/docs/METHODOLOGY.md › The harness]])
- Training ran on an Apple M2 (8 cores, 16 GB RAM, macOS 26.6.2, Python 3.12.14, PyTorch 2.14.0). ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Hardware and measured throughput|course-projects/pacman-dqn/docs/METHODOLOGY.md › Hardware and measured throughput]])
- MPS is ~2.7× faster than CPU for this network, so a 300-episode run costs about 19 minutes rather than the hour a CPU estimate suggests. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Hardware and measured throughput|course-projects/pacman-dqn/docs/METHODOLOGY.md › Hardware and measured throughput]])
- What training bought, most visibly, is the ability to steer. ([[raw/course-projects/pacman-dqn/docs/METHODOLOGY#Behaviour probe|course-projects/pacman-dqn/docs/METHODOLOGY.md › Behaviour probe]])

## Related notes
- [[Deep Q-Network]] — The algorithm the agent uses.
- [[MBA 290T Syllabus]] — Built for this course; the README calls it the Class 3 assignment.
- [[Custom LLM with nanoGPT]] — The other MBA 290T model-training assignment; both tune a learning rate against a fixed evaluation.
- [[UC Berkeley]] — Built at UC Berkeley (Sep 2026).

## Sources
- [[raw/course-projects/pacman-dqn/README|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Ms. Pac-Man DQN — Class 3 Assignment]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/README.md)
- [[raw/website/projects/pacman-dqn|Personal website - projects: Ms. Pac-Man DQN]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/pacman-dqn.md)
- [[raw/course-projects/pacman-dqn/docs/METHODOLOGY|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Methodology: how the three settings were chosen]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/docs/METHODOLOGY.md)
