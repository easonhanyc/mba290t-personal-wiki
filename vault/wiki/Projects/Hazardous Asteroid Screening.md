---
title: Hazardous Asteroid Screening
type: project
summary: This project developed a triage filter to prioritize near-Earth asteroids for observation, as space agencies cannot monitor all of them.
sources:
- path: raw/website/projects/asteroid-screening.md
  source_id: website-projects-asteroid-screening-b2f6998b
  sha256: b2f6998b38c77a1513cb037010e410f60230de5d83ce3d69294a5b04fd496535
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Hazardous Asteroid Screening

This project developed a triage filter to prioritize near-Earth asteroids for observation, as space agencies cannot monitor all of them. The model involved significant data selection, notably removing the most predictive variable based on operational constraints.

## Key facts
- NASA's definition of a hazardous asteroid is made of two variables — and both were columns in the training data. ([[raw/website/projects/asteroid-screening|website/projects/asteroid-screening.md › front matter]])
- The useful model is a triage filter, not an oracle. ([[raw/website/projects/asteroid-screening|website/projects/asteroid-screening.md › front matter]])
- NASA's Center for Near-Earth Object Studies had identified 26,115 near-Earth asteroids and 2,185 potentially dangerous ones. ([[raw/website/projects/asteroid-screening#1. The question behind the question|website/projects/asteroid-screening.md › 1. The question behind the question]])
- NASA's definition of a potentially hazardous asteroid is exact: an Earth Minimum Orbit Intersection Distance of 0.05 au or less, and an absolute magnitude of 22.0 or less. ([[raw/website/projects/asteroid-screening#2. The definition was sitting in the data|website/projects/asteroid-screening.md › 2. The definition was sitting in the data]])
- The raw data was 4,687 asteroid records across 40 variables, of which seventeen survived as predictors. ([[raw/website/projects/asteroid-screening#3. What else came out, and why|website/projects/asteroid-screening.md › 3. What else came out, and why]])
- Four models were evaluated on a 30% holdout: logistic regression, a bagged random forest, XGBoost, and tuned XGBoost. ([[raw/website/projects/asteroid-screening#4. Accuracy was the wrong headline|website/projects/asteroid-screening.md › 4. Accuracy was the wrong headline]])
- Tuning gave up two points of accuracy and bought fifteen points of sensitivity. ([[raw/website/projects/asteroid-screening#4. Accuracy was the wrong headline|website/projects/asteroid-screening.md › 4. Accuracy was the wrong headline]])
- The feature importances came back with absolute magnitude ranked top. ([[raw/website/projects/asteroid-screening#5. The leak that stayed in|website/projects/asteroid-screening.md › 5. The leak that stayed in]])
- The cut-off was found by hand, not optimised. ([[raw/website/projects/asteroid-screening#6. Stated limitations|website/projects/asteroid-screening.md › 6. Stated limitations]])
- Near-Earth asteroids only are in scope, and nothing here extends to meteoroids, comets and other objects without new data. ([[raw/website/projects/asteroid-screening#6. Stated limitations|website/projects/asteroid-screening.md › 6. Stated limitations]])

## Related notes
- [[University of Notre Dame]] — A project for ITAO 40420 (Spring 2022); listed as related work on the Notre Dame entry.
- [[Custom LLM with nanoGPT]] — Both confront leakage: here NASA's definition sat in two input columns; there the training corpus was audited for eval leakage.

## Sources
- [[raw/website/projects/asteroid-screening|Personal website - projects: Hazardous Asteroid Screening]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/asteroid-screening.md)
