---
title: Time Series Analysis
type: concept
summary: Time-series analysis models how a measurement changes over time; in these sources most of the work is making the points in a series comparable before any model is fitted.
sources:
- path: raw/website/projects/formula-1-trends.md
  source_id: website-projects-formula-1-trends-9c8ef2b2
  sha256: 9c8ef2b2753dc0266ce5233731f92c3256f44c39130eb9b496789c8f883b3ef7
- path: raw/website/projects/genai-target-setting.md
  source_id: website-projects-genai-target-setting-e80c6f2c
  sha256: e80c6f2cc4f236432b61aab0a672a4d97e3e8ca393c8431f254a1ae1161288cb
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Time Series Analysis

Time-series analysis models how a measurement changes over time; in these sources most of the work is making the points in a series comparable before any model is fitted. It appears in two projects: a 32-season trend in Formula 1 race speeds, and a linear-trend forecast of pipeline creation used to set AWS Sales' first Generative AI target.

## Key facts

### From website/projects/formula-1-trends.md
- The Formula 1 scrape was not clean: two race times came back in a format inconsistent with the rest and had to be repaired, and a missing driver standing and a missing team standing were filled by checking the source pages by hand. ([[raw/website/projects/formula-1-trends#1. The variable that wasn't in the data|website/projects/formula-1-trends.md › 1. The variable that wasn't in the data]])
- A pooled average of derived speed across every race in a season describes which circuits happened to be on that year's calendar rather than describing the cars. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- To compare 1991 to 2022, the analysis held the track constant, leading to the decision to use only Spain because it had the most complete run and the most stable circuit length across the window. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- Holding the circuit constant left thirty-two data points, a thin time series, chosen deliberately because a small valid comparison beats a large invalid one. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- The Formula 1 project scraped thirty-two seasons (1991–2022) of results pages; the hard part was making any two numbers comparable. ([[raw/website/projects/formula-1-trends|website/projects/formula-1-trends.md › front matter]])
- Six candidates were fitted to the series, including linear, quadratic, cubic, quartic, quartic with an exponential transform, and Holt-Winters exponential smoothing, and they were compared on root mean squared error. ([[raw/website/projects/formula-1-trends#4. The model that won, and why that is worth doubting|website/projects/formula-1-trends.md › 4. The model that won, and why that is worth doubting]])
- The quartic exponential model had the lowest root mean squared error, but it is the result the author trusts least, because the exponential transform changes the scale on which residuals are measured. ([[raw/website/projects/formula-1-trends#4. The model that won, and why that is worth doubting|website/projects/formula-1-trends.md › 4. The model that won, and why that is worth doubting]])

### From website/projects/genai-target-setting.md
- In the GenAI target-setting model, pipeline creation was forecast with a least-squares linear trend fitted only on the six months where the category was genuinely active, then projected forward by region. ([[raw/website/projects/genai-target-setting#3. Forecast something that does have history|website/projects/genai-target-setting.md › 3. Forecast something that does have history]])

## Related notes
- [[Formula 1 Racing Trends]] — Fits six trend models to a 32-point speed series after holding the circuit constant.
- [[GenAI Target Setting]] — Forecasts a leading indicator (pipeline creation) with a linear trend because the target had no history.

## Sources
- [[raw/website/projects/formula-1-trends|Personal website - projects: Formula 1 Racing Trends]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/formula-1-trends.md)
- [[raw/website/projects/genai-target-setting|Personal website - projects: GenAI Target Setting]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/genai-target-setting.md)
