---
title: Deep Learning
type: concept
summary: Deep Learning involves training neural networks with layers of weights and non-linearities, which are optimized using gradient descent to minimize a loss score.
sources:
- path: raw/course-projects/custom-llm/README.md
  source_id: course-projects-custom-llm-readme-11b5c49c
  sha256: 11b5c49c8f481844311ba580dbf1e31268365959af7ea69da8fbd3435fd703a1
- path: raw/course-projects/pacman-dqn/README.md
  source_id: course-projects-pacman-dqn-readme-4b724349
  sha256: 4b724349cd4ac689449f79321b89b5b06e31ce2de3031633fa290309ae100401
- path: raw/course/syllabus.html
  source_id: course-syllabus-b400645c
  sha256: b400645ca89c932ea3f197e8cd04ae595b5c2f6814d758f9dc465c06c54508da
- path: raw/website/projects/pacman-dqn.md
  source_id: website-projects-pacman-dqn-6c3cd8ae
  sha256: 6c3cd8aecdb8a7c7eeceb74b748cdf8a40c1470a571d362d705990531de00d4c
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Deep Learning

Deep Learning involves training neural networks with layers of weights and non-linearities, which are optimized using gradient descent to minimize a loss score. In these sources, it is applied to tasks like playing Ms. Pac-Man using Deep Q-Networks and building custom language models.

## Key facts

### From course-projects/custom-llm/README.md
- A token is a piece of text, an ID is its arbitrary row number, a vector is 64 numbers, and the embedding is the learned vector for that row. ([[raw/course-projects/custom-llm/README#14. What I learned, one limitation, and my next experiment|course-projects/custom-llm/README.md › 14. What I learned, one limitation, and my next experiment]])
- A neural network is characterized by layers of weights with non-linearities, trained by gradient descent. ([[raw/course-projects/custom-llm/README#14. What I learned, one limitation, and my next experiment|course-projects/custom-llm/README.md › 14. What I learned, one limitation, and my next experiment]])
- The learning rate of 1e-05 was used in one experiment, which was derived from a 100-step warmup. ([[raw/course-projects/custom-llm/README#One real gradient and one real weight update|course-projects/custom-llm/README.md › One real gradient and one real weight update]])
- The process of learning involves a loss that scores the prediction, a gradient per parameter, and a small step downhill. ([[raw/course-projects/custom-llm/README#One real gradient and one real weight update|course-projects/custom-llm/README.md › One real gradient and one real weight update]])

### From course-projects/pacman-dqn/README.md
- Deep Q-Network training for Ms. Pac-Man used settings of exploration = 0.10, episodes = 300, and learning rate = 0.0001. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])
- The mean evaluation score for Ms. Pac-Man DQN rose from 492 (untrained) to 906 (trained), representing a +84% increase. ([[raw/course-projects/pacman-dqn/README#Ms. Pac-Man DQN — Class 3 Assignment|course-projects/pacman-dqn/README.md › Ms. Pac-Man DQN — Class 3 Assignment]])

### From course/syllabus.html
- Class 4 covers Deep Learning and Transformers, discussing neurons, activations, and why depth matters. ([[raw/course/syllabus.html|course/syllabus.html › What Each Class Covers]])

### From website/projects/pacman-dqn.md
- The untrained baseline for Ms. Pac-Man DQN was not random but was stuck repeating one move 95.4% of the time. ([[raw/website/projects/pacman-dqn|website/projects/pacman-dqn.md › front matter]])

## Related notes
- [[From Zero to AI Agents]] — From Zero to AI Agents: The course covers deep learning and transformers.
- [[Ms. Pac-Man DQN Implementation]] — Ms. Pac-Man DQN Implementation: The core reinforcement learning technique used to train the agent.
- [[Pac-Man DQN Methodology Study]] — This study details the methodology used to select and test hyperparameters for a Pac-Man DQN agent, relating to the training process described in Deep Learning.
- [[Custom LLM Training Experiments]] — This project details the process of building and evaluating a custom Large Language Model (LLM), which is a form of neural network training discussed in Deep Learning.

## Sources
- [[raw/course-projects/custom-llm/README|MBA 290T project - Custom LLM (Assignment 3): Building a Custom LLM]] — [origin](https://github.com/easonhanyc/mba290t-custom-llm/blob/b1ce9d97c798aa7cb87d8bd0ba0d18bacf9bb445/README.md)
- [[raw/course-projects/pacman-dqn/README|MBA 290T project - Ms. Pac-Man DQN (Assignment 2): Ms. Pac-Man DQN — Class 3 Assignment]] — [origin](https://github.com/easonhanyc/mba290t-pacman-dqn/blob/92dd46e2d25e63e21bb351085e6a781a25b35841/README.md)
- [[raw/course/syllabus.html|MBA 290T course site: Syllabus – From Zero to AI Agents — Seven-Class Edition]] — [origin](https://haas-ai-classes-fall-26.vercel.app/syllabus.html)
- [[raw/website/projects/pacman-dqn|Personal website - projects: Ms. Pac-Man DQN]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/pacman-dqn.md)
