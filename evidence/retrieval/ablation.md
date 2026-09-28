# Retrieval ablation

Same four questions, same 507-passage index, top 6 passages. Rank at which each expected evidence item appears (— = not in the top 6).

| Expected evidence | BM25 only | Vectors only | Hybrid (used) |
|---|---|---|---|
| T1 E1: `syllabus.html` › Attendance | 1 | 2 | 1 |
| T1 E2: `syllabus.html` › Grading | 2 | 1 | 2 |
| T2 E1: `README.md` › Authentication and ownership | — | — | — |
| T2 E2: `secure-networking-tracker.md` › any | 4 | 2 | 2 |
| T3 E1: `amazon-web-services.md` › properties | 6 | — | 5 |
| T3 E2: `action-hub.md` › any | 1 | 1 | 1 |

Raw results: `ablation-bm25.json`, `ablation-vector.json`, `ablation-hybrid.json` in this folder.
