# Retrieval check: ablation-hybrid

Run 2026-09-27T01:20:33. 507 passages indexed; top-6 shown (what ask mode passes to Gemma). No language model is called.

## T1: What share of the final grade is attendance, and how many classes can be missed without penalty?

Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion)

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/course/syllabus.html` › Attendance (must contain 20%, one absence with no penalty) | 1 |
| E2: `vault/raw/course/syllabus.html` › Grading (must contain Attendance, 20%) | 2 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course/syllabus.html:492-494` | MBA 290T: Fundamental of Agentic AI › Attendance | 1 | 2 | E1 |
| 2 | `raw/course/syllabus.html:593-621` | MBA 290T: Fundamental of Agentic AI › Grading | 2 | 1 | E2 |
| 3 | `wiki/Course/MBA 290T Syllabus.md:28-36` | MBA 290T Syllabus › Key facts | 4 | 3 |  |
| 4 | `raw/course/syllabus.html:413-418` | MBA 290T: Fundamental of Agentic AI › Class Schedule | 5 | 4 |  |
| 5 | `wiki/Course/MBA 290T Syllabus.md:21-27` | MBA 290T Syllabus › Key facts | 3 | 8 |  |
| 6 | `raw/course/syllabus.html:498-536` | MBA 290T: Fundamental of Agentic AI › Graded Assignments | 7 | 5 |  |

## T2: In the app I built to track people I meet, what stops one user from seeing someone else's list?

Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion)

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/course-projects/secure-networking-tracker/README.md` › Authentication and ownership (must contain Three independent mechanisms, Row Level Security) | not in top 6 |
| E2: `vault/raw/website/projects/secure-networking-tracker.md` › any (must contain Row Level Security) | 2 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course-projects/secure-networking-tracker/README.md:3-5` | Secure Networking Tracker | 1 | 1 |  |
| 2 | `raw/website/projects/secure-networking-tracker.md:28-30` | (introduction) | 4 | 2 | E2 |
| 3 | `raw/course-projects/secure-networking-tracker/README.md:345-351` | Secure Networking Tracker › Authentication and ownership | 3 | 3 |  |
| 4 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:9-9` | How this app works › 1. The one-paragraph version | 7 | 5 |  |
| 5 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:85-89` | How this app works › 3. The ownership rule › Layer 2 — Row Level Security filters every statement | 2 | 16 |  |
| 6 | `raw/website/projects/secure-networking-tracker.md:77-88` | 2. Where the boundary actually is › The subtle one | 8 | 13 |  |

## T3: What was my job title at Amazon Web Services, and by how much did the Action Hub cut sellers' time-to-insight?

Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion)

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/website/experience/amazon-web-services.md` › properties (must contain Business Intelligence Engineer) | 5 |
| E2: `vault/raw/website/projects/action-hub.md` › any (must contain 70%) | 1 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/website/projects/action-hub.md:1-23` | Properties | 1 | 2 | E2 |
| 2 | `wiki/Projects/Action Hub.md:35-37` | Action Hub › Related notes | 2 | 7 |  |
| 3 | `wiki/Experience/Amazon Web Services.md:21-26` | Amazon Web Services › Key facts | 3 | 6 |  |
| 4 | `wiki/Projects/Action Hub.md:18-18` | Action Hub | 9 | 4 |  |
| 5 | `raw/website/experience/amazon-web-services.md:1-14` | Properties | 6 | 8 | E1 |
| 6 | `raw/website/projects/action-hub.md:28-33` | (introduction) | 12 | 3 | E2 |

## T4: What grade did I receive on the Pac-Man assignment?

Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion)

No supporting passage exists (unsupported question); these are the distractors retrieved.

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course-projects/pacman-dqn/README.md:3-9` | Ms. Pac-Man DQN — Class 3 Assignment | 7 | 2 |  |
| 2 | `wiki/Projects/Ms. Pac-Man DQN.md:24-24` | Ms. Pac-Man DQN | 6 | 4 |  |
| 3 | `wiki/Projects/Ms. Pac-Man DQN.md:29-33` | Ms. Pac-Man DQN › Key facts › From course-projects/pacman-dqn/README.md | 10 | 5 |  |
| 4 | `raw/course-projects/pacman-dqn/README.md:137-138` | Ms. Pac-Man DQN — Class 3 Assignment › What I expected, and what actually happened | 3 | 13 |  |
| 5 | `wiki/Projects/Ms. Pac-Man DQN.md:64-66` | Ms. Pac-Man DQN › Sources | 1 | 18 |  |
| 6 | `raw/course-projects/pacman-dqn/README.md:433-440` | Ms. Pac-Man DQN — Class 3 Assignment › Assignment requirements checklist | 16 | 6 |  |
