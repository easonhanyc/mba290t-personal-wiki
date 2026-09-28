---
title: Formula 1 Racing Trends Analysis
type: project
summary: This project analyzed thirty-two seasons of Formula 1 data to determine if car speeds have increased over time.
sources:
- path: raw/website/projects/formula-1-trends.md
  source_id: website-projects-formula-1-trends-9c8ef2b2
  sha256: 9c8ef2b2753dc0266ce5233731f92c3256f44c39130eb9b496789c8f883b3ef7
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Formula 1 Racing Trends Analysis

This project analyzed thirty-two seasons of Formula 1 data to determine if car speeds have increased over time. The analysis required significant preprocessing to make disparate data points comparable, focusing on derived speed metrics and handling changes in regulations and circuits.

## Key facts
- The variable needed, car speed, is not published by Formula 1. ([[raw/website/projects/formula-1-trends#1. The variable that wasn't in the data|website/projects/formula-1-trends.md › 1. The variable that wasn't in the data]])
- Speed was derived by calculating race distance divided by the winner's completion time, with time values converted to minutes for consistency. ([[raw/website/projects/formula-1-trends#1. The variable that wasn't in the data|website/projects/formula-1-trends.md › 1. The variable that wasn't in the data]])
- The analysis used data scraped from the official results archive covering seasons from 1991 to 2022. ([[raw/website/projects/formula-1-trends#1. The variable that wasn't in the data|website/projects/formula-1-trends.md › 1. The variable that wasn't in the data]])
- To compare seasons, the analysis held the track constant, selecting the Spanish Grand Prix as the only circuit used for the speed analysis. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- The points system changed in 2010, requiring points to be normalized within each era separately before being combined by their mean. ([[raw/website/projects/formula-1-trends#2. Three ways the numbers weren't comparable|website/projects/formula-1-trends.md › 2. Three ways the numbers weren't comparable]])
- The fitted trend line showed that the winner's average speed at Spain rose steadily to around 2005, fell sharply, and recovered partially in the mid-2010s. ([[raw/website/projects/formula-1-trends#3. What the speed curve actually shows|website/projects/formula-1-trends.md › 3. What the speed curve actually shows]])
- Six candidates were fitted to the time series data, including linear, quadratic, cubic, quartic, quartic with an exponential transform, and Holt-Winters exponential smoothing. ([[raw/website/projects/formula-1-trends#4. The model that won, and why that is worth doubting|website/projects/formula-1-trends.md › 4. The model that won, and why that is worth doubting]])
- K-means clustering was used over two features—average annual standing and normalized points—to analyze teams and drivers. ([[raw/website/projects/formula-1-trends#5. Clustering, and what unsupervised output is worth|website/projects/formula-1-trends.md › 5. Clustering, and what unsupervised output is worth]])
- The clustering returned Mercedes as the strongest team of the period, with Ferrari and Red Bull in the same top tier. ([[raw/website/projects/formula-1-trends#5. Clustering, and what unsupervised output is worth|website/projects/formula-1-trends.md › 5. Clustering, and what unsupervised output is worth]])
- The number of clusters was chosen by silhouette score rather than by habit, resulting in three tiers for teams but only two for drivers. ([[raw/website/projects/formula-1-trends#5. Clustering, and what unsupervised output is worth|website/projects/formula-1-trends.md › 5. Clustering, and what unsupervised output is worth]])
- Weather is missing entirely from the data, which means race times reflect conditions that are not accounted for in the trend line. ([[raw/website/projects/formula-1-trends#6. What I'd do differently|website/projects/formula-1-trends.md › 6. What I'd do differently]])
- The two points eras need proper weighting rather than an equal average because drivers and teams competing after 2010 still score higher. ([[raw/website/projects/formula-1-trends#6. What I'd do differently|website/projects/formula-1-trends.md › 6. What I'd do differently]])

## Related notes
- [[Notre Dame Business Analytics Education]] — This project was completed as part of the coursework at the Mendoza College of Business.
- [[Ms. Pac-Man DQN Implementation]] — Both notes involve using a Deep Q-Network for an agent to learn a task.
- [[Time Series Analysis]] — The project involved fitting models to data collected over sequential time periods to identify trends.

## Sources
- [[raw/website/projects/formula-1-trends|Personal website - projects: Formula 1 Racing Trends]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/formula-1-trends.md)
