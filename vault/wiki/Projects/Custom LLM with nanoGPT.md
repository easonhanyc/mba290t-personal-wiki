---
title: Custom LLM with nanoGPT
type: project
summary: 'Building a Custom LLM was an MBA 290T assignment: a small nanoGPT (2 blocks, 4 heads, 64-number embeddings, 48-token context) trained on a classroom corpus and on extended corpora, then scored on a fixed 48-case language eval suite.'
sources:
- path: raw/course-projects/custom-llm/README.md
  source_id: course-projects-custom-llm-readme-11b5c49c
  sha256: 11b5c49c8f481844311ba580dbf1e31268365959af7ea69da8fbd3435fd703a1
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Custom LLM with nanoGPT

Building a Custom LLM was an MBA 290T assignment: a small nanoGPT (2 blocks, 4 heads, 64-number embeddings, 48-token context) trained on a classroom corpus and on extended corpora, then scored on a fixed 48-case language eval suite. The delivered model D reached 40/48 on that suite and 12/16 on a held-out suite written after the corpus was frozen.

## Key facts
- The model is a nanoGPT with 2 blocks, 4 heads, 64-number embeddings and a 48-token context. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Experiment A uses only the classroom corpus, while Experiment B uses the classroom corpus plus 5,005 new passages. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Both Experiment A and Experiment B use 3,000 steps at a learning rate of 0.001. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- The delivered model D scores 40/48 on the unchanged 48-case language eval suite. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- The delivered model D scores 12/16 on a held-out suite written after the corpus was frozen. ([[raw/course-projects/custom-llm/README#One-page summary|course-projects/custom-llm/README.md › One-page summary]])
- Experiment A is reproduced with `python tools/run_experiment.py --experiment starter`. ([[raw/course-projects/custom-llm/README#1. How to run everything|course-projects/custom-llm/README.md › 1. How to run everything]])
- Experiment D is reproduced with `python tools/run_experiment.py --experiment tuned --corpus-dir corpus_seven --lr 0.004`. ([[raw/course-projects/custom-llm/README#1. How to run everything|course-projects/custom-llm/README.md › 1. How to run everything]])
- The delivered model D is defined as using the `corpus_seven`, 3,000 steps, and learning rate 0.004. ([[raw/course-projects/custom-llm/README#Overview of all five experiments|course-projects/custom-llm/README.md › Overview of all five experiments]])
- The corpora compared were the classroom corpus alone, plus a 4-category extension, plus a 7-category extension, and the 7-category extension with unpaired relations; the assignment required the first two. ([[raw/course-projects/custom-llm/README#3. My three choices and my prediction|course-projects/custom-llm/README.md › 3. My three choices and my prediction]])
- The most surprising result was that adding grammar and spatial text made the model better at rephrasings of the original business sentences. ([[raw/course-projects/custom-llm/README#What actually happened|course-projects/custom-llm/README.md › What actually happened]])
- Half the training budget produced no visible difference in sampled text — a concrete reason not to treat "the samples look good" as evidence of learning. ([[raw/course-projects/custom-llm/README|course-projects/custom-llm/README.md › Untrained → halfway → final samples]])

## Related notes
- [[MBA 290T Syllabus]] — Built for this course (repository mba290t-custom-llm).
- [[Deep Learning]] — The concepts this project demonstrates: embeddings, attention, loss and gradient steps.
- [[Ms. Pac-Man DQN]] — The other MBA 290T model-training assignment; both tune a learning rate against a fixed evaluation.
- [[Hazardous Asteroid Screening]] — Both confront leakage: here the corpus was audited for eval leakage; there NASA's definition sat in two input columns.

## Sources
- [[raw/course-projects/custom-llm/README|MBA 290T project - Custom LLM (Assignment 3): Building a Custom LLM]] — [origin](https://github.com/easonhanyc/mba290t-custom-llm/blob/b1ce9d97c798aa7cb87d8bd0ba0d18bacf9bb445/README.md)
