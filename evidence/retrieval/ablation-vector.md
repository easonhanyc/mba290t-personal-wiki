# Retrieval check: ablation-vector

Run 2026-09-27T01:20:32. 507 passages indexed; top-6 shown (what ask mode passes to Gemma). No language model is called.

## T1: What share of the final grade is attendance, and how many classes can be missed without penalty?

Method: EmbeddingGemma vectors only

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/course/syllabus.html` › Attendance (must contain 20%, one absence with no penalty) | 2 |
| E2: `vault/raw/course/syllabus.html` › Grading (must contain Attendance, 20%) | 1 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course/syllabus.html:593-621` | MBA 290T: Fundamental of Agentic AI › Grading | - | 1 | E2 |
| 2 | `raw/course/syllabus.html:492-494` | MBA 290T: Fundamental of Agentic AI › Attendance | - | 2 | E1 |
| 3 | `wiki/Course/MBA 290T Syllabus.md:28-36` | MBA 290T Syllabus › Key facts | - | 3 |  |
| 4 | `raw/course/syllabus.html:413-418` | MBA 290T: Fundamental of Agentic AI › Class Schedule | - | 4 |  |
| 5 | `raw/course/syllabus.html:498-536` | MBA 290T: Fundamental of Agentic AI › Graded Assignments | - | 5 |  |
| 6 | `raw/course/syllabus.html:587-587` | MBA 290T: Fundamental of Agentic AI › Graded Assignments › How Assignments Are Graded | - | 6 |  |

## T2: In the app I built to track people I meet, what stops one user from seeing someone else's list?

Method: EmbeddingGemma vectors only

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/course-projects/secure-networking-tracker/README.md` › Authentication and ownership (must contain Three independent mechanisms, Row Level Security) | not in top 6 |
| E2: `vault/raw/website/projects/secure-networking-tracker.md` › any (must contain Row Level Security) | 2 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course-projects/secure-networking-tracker/README.md:3-5` | Secure Networking Tracker | - | 1 |  |
| 2 | `raw/website/projects/secure-networking-tracker.md:28-30` | (introduction) | - | 2 | E2 |
| 3 | `raw/course-projects/secure-networking-tracker/README.md:345-351` | Secure Networking Tracker › Authentication and ownership | - | 3 |  |
| 4 | `raw/course-projects/secure-networking-tracker/README.md:74-76` | Secure Networking Tracker › Screenshots › Two accounts, side by side | - | 4 |  |
| 5 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:9-9` | How this app works › 1. The one-paragraph version | - | 5 |  |
| 6 | `wiki/Projects/Secure Networking Tracker.md:39-42` | Secure Networking Tracker › Key facts › From course-projects/secure-networking-tracker/docs/how-it-works.md | - | 6 |  |

## T3: What was my job title at Amazon Web Services, and by how much did the Action Hub cut sellers' time-to-insight?

Method: EmbeddingGemma vectors only

| Expected evidence | Found at rank |
|---|---|
| E1: `vault/raw/website/experience/amazon-web-services.md` › properties (must contain Business Intelligence Engineer) | not in top 6 |
| E2: `vault/raw/website/projects/action-hub.md` › any (must contain 70%) | 1 |

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/website/projects/action-hub.md:24-26` | (introduction) | - | 1 | E2 |
| 2 | `raw/website/projects/action-hub.md:1-23` | Properties | - | 2 | E2 |
| 3 | `raw/website/projects/action-hub.md:28-33` | (introduction) | - | 3 | E2 |
| 4 | `wiki/Projects/Action Hub.md:18-18` | Action Hub | - | 4 |  |
| 5 | `wiki/Projects/Action Hub.md:21-26` | Action Hub › Key facts | - | 5 |  |
| 6 | `wiki/Experience/Amazon Web Services.md:21-26` | Amazon Web Services › Key facts | - | 6 |  |

## T4: What grade did I receive on the Pac-Man assignment?

Method: EmbeddingGemma vectors only

No supporting passage exists (unsupported question); these are the distractors retrieved.

| Rank | Passage | Section | BM25 rank | Vector rank | Matches |
|---|---|---|---|---|---|
| 1 | `raw/course-projects/pacman-dqn/README.md:452-457` | Ms. Pac-Man DQN — Class 3 Assignment › How this maps to the grading components | - | 1 |  |
| 2 | `raw/course-projects/pacman-dqn/README.md:3-9` | Ms. Pac-Man DQN — Class 3 Assignment | - | 2 |  |
| 3 | `raw/course-projects/pacman-dqn/README.md:461-472` | Ms. Pac-Man DQN — Class 3 Assignment › Honest reporting notes | - | 3 |  |
| 4 | `wiki/Projects/Ms. Pac-Man DQN.md:24-24` | Ms. Pac-Man DQN | - | 4 |  |
| 5 | `wiki/Projects/Ms. Pac-Man DQN.md:29-33` | Ms. Pac-Man DQN › Key facts › From course-projects/pacman-dqn/README.md | - | 5 |  |
| 6 | `raw/course-projects/pacman-dqn/README.md:433-440` | Ms. Pac-Man DQN — Class 3 Assignment › Assignment requirements checklist | - | 6 |  |
