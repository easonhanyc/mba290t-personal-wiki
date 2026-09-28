---
title: Custom LLM Training Experiments
type: project
summary: This project details the process of building and evaluating a custom Large Language Model (LLM) using nanoGPT.
sources:
- path: raw/course-projects/custom-llm/README.md
  source_id: course-projects-custom-llm-readme-11b5c49c
  sha256: 11b5c49c8f481844311ba580dbf1e31268365959af7ea69da8fbd3435fd703a1
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Custom LLM Training Experiments

This project details the process of building and evaluating a custom Large Language Model (LLM) using nanoGPT. Several experiments were conducted, varying corpus size, learning rates, and training steps to observe the model's performance on language evaluation suites.

## Key facts
- nanoGPT has 2 blocks, 4 heads, 64-number embeddings, and a 48-token context. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Experiment A uses only the classroom corpus, while Experiment B uses the classroom corpus plus 5,005 new passages. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Both Experiment A and Experiment B use 3,000 steps at a learning rate of 0.001. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- The delivered model D has seven taught categories and a learning rate of 0.004. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- The delivered model D scores 40/48 on the unchanged 48-case language eval suite. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- The delivered model D scores 12/16 on a held-out suite written after the corpus was frozen. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Reproduce experiment A can be done using the command python tools/run_experiment.py --experiment starter. ([[raw/course-projects/custom-llm/README#1. How to run everything|course-projects/custom-llm/README.md › 1. How to run everything]])
- Reproduce experiment D requires the command python tools/run_experiment.py --experiment tuned --corpus-dir corpus_seven --lr 0.004. ([[raw/course-projects/custom-llm/README#1. How to run everything|course-projects/custom-llm/README.md › 1. How to run everything]])
- The delivered model D is defined as using the `corpus_seven`, 3,000 steps, and learning rate 0.004. ([[raw/course-projects/custom-llm/README#Overview of all five experiments|course-projects/custom-llm/README.md › Overview of all five experiments]])
- The choice of corpus was classroom; + 4-category; + 7-category; + 7-category with unpaired relations because the assignment requires the first two. ([[raw/course-projects/custom-llm/README#3. My three choices and my prediction|course-projects/custom-llm/README.md › 3. My three choices and my prediction]])
- The most surprising result was that adding grammar and spatial text made the model better at rephrasings of the original business sentences. ([[raw/course-projects/custom-llm/README#What actually happened|course-projects/custom-llm/README.md › What actually happened]])
- Half the training budget produced no visible difference in sampled text — a concrete reason not to treat "the samples look good" as evidence of learning. ([[raw/course-projects/custom-llm/README|course-projects/custom-llm/README.md › Untrained → halfway → final samples]])

## Related notes
- [[From Zero to AI Agents]] — Both notes relate to the process of building and evaluating AI systems.
- [[Ms. Pac-Man DQN Implementation]] — Both notes detail training a model using a specific architecture (DQN/LLM).

## Sources
- [[raw/course-projects/custom-llm/README|MBA 290T project - Custom LLM (Assignment 3): Building a Custom LLM]] — [origin](https://github.com/easonhanyc/mba290t-custom-llm/blob/b1ce9d97c798aa7cb87d8bd0ba0d18bacf9bb445/README.md)
