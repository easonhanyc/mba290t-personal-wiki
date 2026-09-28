---
title: Job Search Agent
type: project
summary: This project is a daily scanner designed to find PM internships for Summer 2027.
sources:
- path: raw/website/projects/job-search-agent.md
  source_id: website-projects-job-search-agent-13c384c5
  sha256: 13c384c532b962b3a41bfa1d79a91f5daa653816a0edcc7586b88556b4a65b73
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Job Search Agent

This project is a daily scanner designed to find PM internships for Summer 2027. It focuses on ranking relevant roles over simply matching keywords to ensure high-quality, focused output.

## Key facts
- The agent scans roughly 29,400 postings in about 50 seconds every weekday, and opens a GitHub issue only when something new appears. ([[raw/website/projects/job-search-agent|website/projects/job-search-agent.md › front matter]])
- The output is capped at two roles per company, and a run that reports nothing is considered a successful run. ([[raw/website/projects/job-search-agent|website/projects/job-search-agent.md]])
- The fix for weighting issues was to make the product-role signal deliberately dominant, weighting it 100 against 45 for "explicitly hires MBAs" and 15 for strategy/BizOps. ([[raw/website/projects/job-search-agent|website/projects/job-search-agent.md › 1. The decision I'd point to: ranking, not matching]])
- The agent matches only on a narrow set of high-signal phrases like "MBA students" or "pursuing an MBA" from descriptions, not general keywords. ([[raw/website/projects/job-search-agent#2. Matching on titles, not descriptions|website/projects/job-search-agent.md › 2. Matching on titles, not descriptions]])
- The gate for the daily scan is set to "at or after noon Pacific, if today has not already run," using committed run logs to prevent missed days. ([[raw/website/projects/job-search-agent#3. Silence has to be trustworthy|website/projects/job-search-agent.md › 3. Silence has to be trustworthy]])
- Delivery is via a GitHub issue, which uses the GITHUB_TOKEN automatically, meaning there is nothing to configure or rotate. ([[raw/website/projects/job-search-agent#4. Choosing a delivery channel with no secrets|website/projects/job-search-agent.md › 4. Choosing a delivery channel with no secrets]])
- LinkedIn, Indeed and Handshake are not covered because they are login-gated or prohibit scraping. ([[raw/website/projects/job-search-agent#5. Known limits|website/projects/job-search-agent.md › 5. Known limits]])

## Related notes
- [[Action Hub]] — Both rank a long list and cap it on purpose: two roles per company here, fifty alerts per seller there.
- [[TripMatch Rides Board]] — Another independent project from Aug–Sep 2026, built end to end alone.

## Sources
- [[raw/website/projects/job-search-agent|Personal website - projects: Job Search Agent]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/job-search-agent.md)
