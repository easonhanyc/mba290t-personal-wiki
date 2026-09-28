# Re-ingestion check (2026-09-27 01:06)

Same sources ingested again after the wiki was cleaned up and reviewed.

```
$ wiki ingest vault/raw
= raw/course/syllabus.html: unchanged (sha256 b400645ca89c), notes up to date: MBA 290T Syllabus, Deep Learning
= raw/course-projects/custom-llm/README.md: unchanged (sha256 11b5c49c8f48), notes up to date: Custom LLM with nanoGPT, Deep Learning
= raw/course-projects/pacman-dqn/README.md: unchanged (sha256 4b724349cd4a), notes up to date: Ms. Pac-Man DQN, Deep Learning, Deep Q-Network
= raw/course-projects/pacman-dqn/docs/METHODOLOGY.md: unchanged (sha256 b14e34e7414b), notes up to date: Ms. Pac-Man DQN
= raw/course-projects/secure-networking-tracker/README.md: unchanged (sha256 4b2dc6a22bd0), notes up to date: Secure Networking Tracker
= raw/course-projects/secure-networking-tracker/docs/how-it-works.md: unchanged (sha256 5ab70ce209d7), notes up to date: Secure Networking Tracker
= raw/website/experience/amazon-web-services.md: unchanged (sha256 6b6451e8b3a0), notes up to date: Amazon Web Services
= raw/website/experience/clean-shores.md: unchanged (sha256 1fa66d70f081), notes up to date: Seaside Sustainability
= raw/website/experience/idg-capital.md: unchanged (sha256 a3dca4538202), notes up to date: IDG Capital
= raw/website/experience/notre-dame.md: unchanged (sha256 3814314d1781), notes up to date: University of Notre Dame
= raw/website/experience/tiktok.md: unchanged (sha256 506c7ec1a979), notes up to date: TikTok Internship
= raw/website/experience/uc-berkeley.md: unchanged (sha256 c2a9c5038e7f), notes up to date: UC Berkeley
= raw/website/projects/action-hub.md: unchanged (sha256 c6c9d5e99239), notes up to date: Action Hub
= raw/website/projects/allowlist.md: unchanged (sha256 4567a2efe10e), notes up to date: Allowlist Data Access App
= raw/website/projects/asteroid-screening.md: unchanged (sha256 b2f6998b38c7), notes up to date: Hazardous Asteroid Screening
= raw/website/projects/datafest-2023.md: unchanged (sha256 308b95c82686), notes up to date: DataFest 2023
= raw/website/projects/formula-1-trends.md: unchanged (sha256 9c8ef2b2753d), notes up to date: Formula 1 Racing Trends, Time Series Analysis
= raw/website/projects/genai-adoption-program.md: unchanged (sha256 24dc0351e0af), notes up to date: GenAI Adoption Program
= raw/website/projects/genai-target-setting.md: unchanged (sha256 e80c6f2cc4f2), notes up to date: GenAI Target Setting, Time Series Analysis
= raw/website/projects/job-search-agent.md: unchanged (sha256 13c384c532b9), notes up to date: Job Search Agent
= raw/website/projects/pacman-dqn.md: unchanged (sha256 6c3cd8aecdb8), notes up to date: Ms. Pac-Man DQN, Deep Learning, Deep Q-Network
= raw/website/projects/pr-automation.md: unchanged (sha256 cfba08280fda), notes up to date: Pull-Request Automation
= raw/website/projects/secure-networking-tracker.md: unchanged (sha256 fb3996868f0d), notes up to date: Secure Networking Tracker
= raw/website/projects/tripmatch.md: unchanged (sha256 c8542a2ca92b), notes up to date: TripMatch Rides Board

Ingest finished in 6s with gemma-4-e4b-it-qat-q4_0 (local): 24 unchanged
Index: 507 passages (24 sources, 23 reviewed notes); 119 newly embedded. index.md and Source Catalog.md rebuilt.
```

Notes before: 23, after: 23.
Every note file is byte-identical before and after (sha256 compared): no duplicates, no renamed or regenerated notes.

File list after re-ingest:
```
wiki/Concepts/Deep Learning.md
wiki/Concepts/Deep Q-Network.md
wiki/Concepts/Time Series Analysis.md
wiki/Course/MBA 290T Syllabus.md
wiki/Experience/Amazon Web Services.md
wiki/Experience/IDG Capital.md
wiki/Experience/Seaside Sustainability.md
wiki/Experience/TikTok Internship.md
wiki/Experience/UC Berkeley.md
wiki/Experience/University of Notre Dame.md
wiki/Projects/Action Hub.md
wiki/Projects/Allowlist Data Access App.md
wiki/Projects/Custom LLM with nanoGPT.md
wiki/Projects/DataFest 2023.md
wiki/Projects/Formula 1 Racing Trends.md
wiki/Projects/GenAI Adoption Program.md
wiki/Projects/GenAI Target Setting.md
wiki/Projects/Hazardous Asteroid Screening.md
wiki/Projects/Job Search Agent.md
wiki/Projects/Ms. Pac-Man DQN.md
wiki/Projects/Pull-Request Automation.md
wiki/Projects/Secure Networking Tracker.md
wiki/Projects/TripMatch Rides Board.md
```

Forcing a re-read shows which notes it would update (dry run, no model call):
```
$ wiki ingest --force --dry-run vault/raw/website/projects/tripmatch.md vault/raw/course-projects/pacman-dqn/docs/METHODOLOGY.md
+ raw/website/projects/tripmatch.md: 2347 words, 10 sections
    dry run: would update wiki/Projects/TripMatch Rides Board.md
+ raw/course-projects/pacman-dqn/docs/METHODOLOGY.md: 1219 words, 9 sections
    dry run: would update wiki/Projects/Ms. Pac-Man DQN.md
```
Both map to their existing readable notes (the methodology file to the merged Ms. Pac-Man DQN note), so a forced re-ingest updates those notes in place; notes marked reviewed only get new facts appended under 'From <source>' and flagged needs_review.

## 2026-09-28 15:11 — after fix 10 (merged subjects are redirected)

The concept pass that re-created 'Agentic AI' during the offline ingest, run again on the real vault:
```
  concept 'Agentic AI' was merged away or renamed earlier; not re-created
model calls: 0 | notes created: none
```

```
$ wiki ingest vault/raw

Ingest finished in 1s with gemma-4-e4b-it-qat-q4_0 (local): 25 unchanged
Index: 520 passages (25 sources, 24 reviewed notes); 8 newly embedded. index.md and Source Catalog.md rebuilt.
```
All 24 note files byte-identical before and after; 'Agentic AI' not re-created.
