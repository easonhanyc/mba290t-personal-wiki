---
title: GenAI Target Setting
type: project
summary: This project involved setting the first annual target for a business with almost no history by forecasting a leading indicator instead of the final goal.
sources:
- path: raw/website/projects/genai-target-setting.md
  source_id: website-projects-genai-target-setting-e80c6f2c
  sha256: e80c6f2cc4f236432b61aab0a672a4d97e3e8ca393c8431f254a1ae1161288cb
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# GenAI Target Setting

This project involved setting the first annual target for a business with almost no history by forecasting a leading indicator instead of the final goal. The methodology used 55,000 data points and four scenario simulations, emphasizing a quarterly review cadence to correct the initial target.

## Key facts
- 2024 was the first year AWS Sales carried a Generative AI goal. ([[raw/website/projects/genai-target-setting#1. How a goal becomes a number|website/projects/genai-target-setting.md › 1. How a goal becomes a number]])
- The model forecast a leading indicator that did have history and converted through it. ([[raw/website/projects/genai-target-setting|website/projects/genai-target-setting.md]])
- The model was built across 55,000 data points and four scenario simulations. ([[raw/website/projects/genai-target-setting|website/projects/genai-target-setting.md]])
- The first real decision was to stop trying to forecast the target metric directly. ([[raw/website/projects/genai-target-setting#2. Why the obvious approach fails|website/projects/genai-target-setting.md › 2. Why the obvious approach fails]])
- Pipeline creation had been running long enough to have a real series. ([[raw/website/projects/genai-target-setting#3. Forecast something that does have history|website/projects/genai-target-setting.md › 3. Forecast something that does have history]])
- The model forecasts pipeline creation using a least-squares linear trend fitted only on the months where the category was genuinely active. ([[raw/website/projects/genai-target-setting#3. Forecast something that does have history|website/projects/genai-target-setting.md › 3. Forecast something that does have history]])
- The median open-to-close for opportunities in this category was about three months, so pipeline created in month N lands in month N+3. ([[raw/website/projects/genai-target-setting#3. Forecast something that does have history|website/projects/genai-target-setting.md › 3. Forecast something that does have history]])
- Attach and win rates came from the later months only — the first period with enough launches per month to compute a rate that wasn't noise. ([[raw/website/projects/genai-target-setting#4. The judgment calls inside that|website/projects/genai-target-setting.md › 4. The judgment calls inside that]])
- A single blended rate would have quietly misallocated quota — over-targeting regions that convert poorly and under-targeting the ones that convert well. ([[raw/website/projects/genai-target-setting#4. The judgment calls inside that|website/projects/genai-target-setting.md › 4. The judgment calls inside that]])
- Four scenario simulations were run as sensitivity analysis across the model's assumptions. ([[raw/website/projects/genai-target-setting#5. What the scenarios are for|website/projects/genai-target-setting.md › 5. What the scenarios are for]])
- The deliverable was not the target, but the target plus a quarterly review cadence. ([[raw/website/projects/genai-target-setting|website/projects/genai-target-setting.md › 6. The part that mattered most: planning to be wrong]])

## Related notes
- [[Amazon Web Services]] — Built in this role at AWS (2024).
- [[Time Series Analysis]] — Its forecast is a least-squares linear trend on six months of pipeline history.

## Sources
- [[raw/website/projects/genai-target-setting|Personal website - projects: GenAI Target Setting]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/genai-target-setting.md)
