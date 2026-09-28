---
title: Time Series Analysis
type: concept
summary: Time Series Analysis involves analyzing data points collected over time, often requiring significant preprocessing to ensure comparability across different data points or models.
sources:
- path: raw/website/projects/formula-1-trends.md
  source_id: website-projects-formula-1-trends-9c8ef2b2
  sha256: 9c8ef2b2753dc0266ce5233731f92c3256f44c39130eb9b496789c8f883b3ef7
- path: raw/website/projects/genai-target-setting.md
  source_id: website-projects-genai-target-setting-e80c6f2c
  sha256: e80c6f2cc4f236432b61aab0a672a4d97e3e8ca393c8431f254a1ae1161288cb
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Time Series Analysis

Time Series Analysis involves analyzing data points collected over time, often requiring significant preprocessing to ensure comparability across different data points or models. In these sources, it appears in projects involving trend modeling, forecasting, and the critical step of making derived metrics comparable.

## Key facts

### From website/projects/formula-1-trends.md
- The variable that wasn't in the data required manual repair because two race times came back in a format inconsistent with the rest, and missing driver and team standings were filled by checking source pages by hand. ([[raw/website/projects/formula-1-trends#1. The variable that wasn't in the data|website/projects/formula-1-trends.md › 1. The variable that wasn't in the data]])
- A pooled average of derived speed across every race in a season describes which circuits happened to be on that year's calendar rather than describing the cars. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- To compare 1991 to 2022, the analysis held the track constant, leading to the decision to use only Spain because it had the most complete run and the most stable circuit length across the window. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- The analysis used thirty-two data points, which was considered a thin time series, and the author chose this deliberately because a small valid comparison beats a large invalid one. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- The project involved scraping thirty-two seasons from Formula 1's results pages, spanning 1991–2022, and the hardest part was making any two numbers comparable. ([[raw/website/projects/formula-1-trends|website/projects/formula-1-trends.md › front matter]])
- Six candidates were fitted to the series, including linear, quadratic, cubic, quartic, quartic with an exponential transform, and Holt-Winters exponential smoothing, and they were compared on root mean squared error. ([[raw/website/projects/formula-1-trends#4. The model that won, and why that is worth doubting|website/projects/formula-1-trends.md › 4. The model that won, and why that is worth doubting]])
- The quartic exponential model was the one that came out lowest when compared on root mean squared error. ([[raw/website/projects/formula-1-trends#4. The model that won, and why that is worth doubting|website/projects/formula-1-trends.md › 4. The model that won, and why that is worth doubting]])

### From website/projects/genai-target-setting.md
- Pipeline creation was forecasted using a least-squares linear trend fitted only on the six months where the category was genuinely active, and then projected forward by region. ([[raw/website/projects/genai-target-setting#3. Forecast something that does have history|website/projects/genai-target-setting.md › 3. Forecast something that does have history]])

## Related notes
- [[Formula 1 Racing Trends Analysis]] — Formula 1 Racing Trends Analysis: The project involved fitting models to data collected over sequential time periods to identify trends.
- [[GenAI Target Setting Methodology]] — GenAI Target Setting Methodology: The use of linear trend fitting on historical data to project future values.

## Sources
- [[raw/website/projects/formula-1-trends|Personal website - projects: Formula 1 Racing Trends]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/formula-1-trends.md)
- [[raw/website/projects/genai-target-setting|Personal website - projects: GenAI Target Setting]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/genai-target-setting.md)
