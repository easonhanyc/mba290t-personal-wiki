---
title: Deep Learning
type: concept
summary: 'Deep learning trains layered networks of weights with non-linearities by gradient descent: a loss scores each prediction and the gradient says which way to move every parameter.'
sources:
- path: raw/course-projects/custom-llm/README.md
  source_id: course-projects-custom-llm-readme-11b5c49c
  sha256: 11b5c49c8f481844311ba580dbf1e31268365959af7ea69da8fbd3435fd703a1
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:59:45'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Deep Learning

Deep learning trains layered networks of weights with non-linearities by gradient descent: a loss scores each prediction and the gradient says which way to move every parameter. In these sources it is shown concretely in the custom nanoGPT project, from turning text into token IDs and embeddings to a single measured weight update.

## Key facts
- In the project's nanoGPT, the parameters are arranged in layers: an embedding table, two transformer blocks (each with 4 attention heads and a small MLP), and an output layer mapping 64 dimensions back to vocabulary scores. ([[raw/course-projects/custom-llm/README#What makes it a neural network, and what attention does|course-projects/custom-llm/README.md › What makes it a neural network, and what attention does]])
- Attention allows the prediction at each position to be a weighted blend of earlier positions. ([[raw/course-projects/custom-llm/README#What makes it a neural network, and what attention does|course-projects/custom-llm/README.md › What makes it a neural network, and what attention does]])
- A causal mask sets future positions to -inf before the softmax, preventing the model from looking at future tokens during training. ([[raw/course-projects/custom-llm/README#What makes it a neural network, and what attention does|course-projects/custom-llm/README.md › What makes it a neural network, and what attention does]])
- A token is a piece of text, an ID is its arbitrary row number, a vector is 64 numbers, and the embedding is the learned vector for that row. ([[raw/course-projects/custom-llm/README#14. What I learned, one limitation, and my next experiment|course-projects/custom-llm/README.md › 14. What I learned, one limitation, and my next experiment]])
- A neural network is characterized by layers of weights with non-linearities, trained by gradient descent, where the loss scores each next-token prediction and the gradient dictates parameter movement. ([[raw/course-projects/custom-llm/README#14. What I learned, one limitation, and my next experiment|course-projects/custom-llm/README.md › 14. What I learned, one limitation, and my next experiment]])
- The gradient answers whether increasing a specific number would raise or lower the loss, and the weight update is the action taken to lower the loss. ([[raw/course-projects/custom-llm/README#One real gradient and one real weight update|course-projects/custom-llm/README.md › One real gradient and one real weight update]])
- The learning rate at step 0 is 1e-05, not 0.001, because step 0 is the first step of a 100-step warmup (0.001 × 1/100). ([[raw/course-projects/custom-llm/README#One real gradient and one real weight update|course-projects/custom-llm/README.md › One real gradient and one real weight update]])
- The corpus is the pile of text the model may learn from, which is cut into passages of at most 47 word tokens and then split 90/10. ([[raw/course-projects/custom-llm/README|course-projects/custom-llm/README.md › Corpus → passage → tokens → IDs]])

## Related notes
- [[Custom LLM with nanoGPT]] — The project these facts come from: a small nanoGPT language model built for MBA 290T.
- [[Deep Q-Network]] — Another neural-network method in this wiki; there the network estimates action values, not next tokens.
- [[MBA 290T Syllabus]] — Class 4 of the course covers deep learning and transformers.

## Sources
- [[raw/course-projects/custom-llm/README|MBA 290T project - Custom LLM (Assignment 3): Building a Custom LLM]] — [origin](https://github.com/easonhanyc/mba290t-custom-llm/blob/b1ce9d97c798aa7cb87d8bd0ba0d18bacf9bb445/README.md)
