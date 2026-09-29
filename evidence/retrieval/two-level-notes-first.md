# Retrieval experiment: two-level (notes first, then their sources)

Run 2026-09-28T20:47:23, 520 passages. Ask gives Gemma the top 6, so a position above 6 means Gemma never sees the passage. Script: `scripts/retrieval_two_level.py`.

| Notes kept | Test | Notes chosen at level 1 | Passages searched at level 2 | Expected evidence: global / level 2 only / fused |
|---|---|---|---|---|
| 1 | T1 | MBA 290T Syllabus | 37 | E1: 1 / 1 / 1; E2: 2 / 2 / 2 |
| 1 | T2 | Allowlist Data Access App | 14 | E1: 30 / — / 37; E2: 2 / — / 11 |
| 1 | T3 | Action Hub | 16 | E1: 5 / — / 18; E2: 1 / 1 / 1 |
| 1 | T4 | Ms. Pac-Man DQN | 61 | n/a (unsupported) |
| 2 | T1 | MBA 290T Syllabus, Job Search Agent | 49 | E1: 1 / 1 / 1; E2: 2 / 2 / 2 |
| 2 | T2 | Allowlist Data Access App, Secure Networking Tracker | 86 | E1: 30 / 33 / 31; E2: 2 / 2 / 2 |
| 2 | T3 | Action Hub, Amazon Web Services | 21 | E1: 5 / 7 / 6; E2: 1 / 1 / 1 |
| 2 | T4 | Ms. Pac-Man DQN, Deep Q-Network | 65 | n/a (unsupported) |
| 3 | T1 | MBA 290T Syllabus, Job Search Agent, Formula 1 Racing Trends | 66 | E1: 1 / 1 / 1; E2: 2 / 2 / 2 |
| 3 | T2 | Allowlist Data Access App, Secure Networking Tracker, Action Hub | 102 | E1: 30 / 32 / 31; E2: 2 / 2 / 2 |
| 3 | T3 | Action Hub, Amazon Web Services, GenAI Adoption Program | 35 | E1: 5 / 6 / 5; E2: 1 / 1 / 1 |
| 3 | T4 | Ms. Pac-Man DQN, Deep Q-Network, MBA 290T Syllabus | 102 | n/a (unsupported) |

— = not found among the ranked candidates.
