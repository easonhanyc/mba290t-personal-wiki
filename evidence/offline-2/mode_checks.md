# Mode-boundary checks

Label `offline-2`, 2026-09-28T21:12:24. Execution: local (llama.cpp on 127.0.0.1), model `gemma-4-e4b-it-qat-q4_0`; internet: **offline**.

## M1: casual chat, capabilities

Expected: accurate capabilities and a suggested starting point; no notes lookup, no citations, no insufficient-evidence refusal.

**you ›** what can you help me with?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 5.77 s._

**Wren ›**

> I'm here to help you organize your thoughts, draft materials, and keep track of your work for the Haas program. Think of me as your personal sounding board and organizational assistant.
>
> Specifically, I can help you with:
>
> *   **Brainstorming and Drafting:** Developing ideas for essays, projects, or presentations.
> *   **Structuring and Rewriting:** Taking rough notes and turning them into polished, concise drafts.
> *   **Information Retrieval:** Looking up specific details in your project notes or wiki when you need quick facts.
> *   **Planning:** Helping you break down large tasks into manageable next steps.
>
> What’s on your plate today?

**you ›** what can we do?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 6.29 s._

**Wren ›**

> Since you're asking generally, here are a few concrete things we can tackle right now, depending on what you're working on:
>
> 1.  **Review/Drafting:** If you have a specific essay prompt, project outline, or email you're working on, paste it here, and we can refine it.
> 2.  **Information Retrieval:** If you need to check on a specific project detail, like a deadline or a key finding, tell me the topic, and I can check your notes [N1].
> 3.  **Brainstorming:** If you're stuck on a concept—say, how to frame a specific challenge in a case study—we can brainstorm angles.
>
> Do any of those sound useful, or is there something else on your mind?

Chat log with exact messages: `runs/chat-20260928-211236-137.jsonl`

Assessment: Partly failed: a stray [N1] tag. Both turns were answered with no notes lookup, the capabilities were accurate, each ended with a starting point, and neither said "insufficient evidence". But the second answer ended a sentence with "[N1]" although no notes were supplied (the CLI run in step 6 did the same in its first answer): a citation that points at nothing, which this check expects not to see. The dry run, the first offline run and the online run had no stray tags. Fixed afterwards (fix 16): the harness removes a note tag when no notes were supplied and says so. Re-run three times with the local model (internet on, not offline) in evidence/local-after-fix16/: the model emitted [N1] once, and the harness removed it and reported the removal.

## M2: conversational follow-up

Expected: second answer is a shorter version of the first plan (uses conversation history).

**you ›** Draft a short plan for my week: I need to finish Assignment 4 and prep for PM internship applications.

_Harness routing: no notes lookup — drafting/planning from what you said: no personal facts needed; 5.96 s._

**Wren ›**

> Here is a draft plan to tackle both Assignment 4 and your PM applications.
>
> **Goal:** Finish Assignment 4 and make significant progress on PM applications this week.
>
> *   **Assignment 4:** Dedicate the first half of the week to deep work on this. Break it down into smaller chunks (e.g., research, drafting, review).
> *   **PM Applications:** Spend the second half of the week focusing on tailoring your materials and applying.
> *   **Buffer/Review:** Keep a small block of time for review, catching up, or tackling whichever task is lagging.
>
> Let me know if you want me to flesh out specific tasks for either area, like breaking down Assignment 4's requirements or drafting a cover letter template.

**you ›** make that shorter

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 2.76 s._

**Wren ›**

> Here is a tighter version:
>
> *   **Mon-Wed:** Finish Assignment 4 (Deep Work).
> *   **Thu-Fri:** PM Application Prep/Submissions.
> *   **Weekend:** Buffer/Review.
>
> Does that work, or should I focus on detailing the first few steps for Assignment 4?

Chat log with exact messages: `runs/chat-20260928-211248-211.jsonl`

Assessment: Pass. The week plan was drafted without a notes lookup, and "make that shorter" condensed the same plan (Mon–Wed Assignment 4, Thu–Fri PM applications, weekend buffer) from the conversation.

## M3: raw search

Expected: original passages with source paths; zero model calls; also works with the Gemma server stopped.

Gemma server running during this search: **False**. Model calls: **0**. Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion). Time: 0.025 s.

| # | Passage | Section |
|---|---|---|
| 1 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:52-83` | How this app works › 3. The ownership rule › Layer 2 — Row Level Security filters every statement |
| 2 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:85-89` | How this app works › 3. The ownership rule › Layer 2 — Row Level Security filters every statement |
| 3 | `wiki/Projects/Secure Networking Tracker.md:39-42` | Secure Networking Tracker › Key facts › From course-projects/secure-networking-tracker/docs/how-it-works.md |
| 4 | `raw/website/projects/secure-networking-tracker.md:46-73` | 2. Where the boundary actually is |
| 5 | `raw/course-projects/secure-networking-tracker/README.md:318-343` | Secure Networking Tracker › Authentication and ownership |
| 6 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:9-9` | How this app works › 1. The one-paragraph version |

First passage, verbatim:

> ```sql
> ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;
> ALTER TABLE public.contacts FORCE  ROW LEVEL SECURITY;
> ```
> `ENABLE` turns policies on. `FORCE` also applies them to the table's *owner* — without it, `neondb_owner` would bypass every policy.
> Four policies, one per operation, all for the `authenticated` role:
> ```sql
> CREATE POLICY contacts_select_own ON public.contacts
>   FOR SELECT TO authenticated
>   USING ((SELECT auth.user_id()) = user_id);
>
> CREATE POLICY contacts_insert_own ON public.contacts
>   FOR INSERT TO authenticated
>   WITH CHECK ((SELECT auth.user_id()) = user_id);
>
> CREATE POLICY contacts_update_own ON public.contacts
>   FOR UPDATE TO authenticated
>   USING      ((SELECT auth.user_id()) = user_id)
>   WITH CHECK ((SELECT auth.user_id()) = user_id);
>
> CREATE POLICY contacts_delete_own ON public.contacts
>   FOR DELETE TO authenticated
>   USING ((SELECT auth.user_id()) = user_id);
> ```
> **`USING` vs `WITH CHECK` — the distinction to have ready:**
> - `USING` filters rows that already exist. It answers *"which rows may this statement see or touch?"* It is silently added to `SELECT`, `UPDATE` and `DELETE` as an extra `WHERE` clause.
> - `WITH CHECK` inspects the row *as it will be after the write*. It answers *"is this row allowed to exist looking like that?"* It applies to `INSERT` and `UPDATE`.

Assessment: Pass. With the Gemma server stopped, search returned six original passages with paths and line numbers in 0.025 s and made zero model calls.

## M4: ask ignores chat history

Expected: ask reports insufficient evidence; the saved ask prompt contains no chat text.

**you ›** By the way, my favorite programming language is Rust.

_Harness routing: no notes lookup — model router decided no notes needed; 5.33 s._

**Wren ›**

> Got it. Rust. Good to know.
>
> Is there anything specific you'd like to work on today, or should I just keep tabs on things?

Chat log with exact messages: `runs/chat-20260928-211259-230.jsonl`

Then, separately: `wiki ask "What is my favorite programming language?"`

> Insufficient evidence: The provided passages describe course material, project structures, and evaluation methods for a course, but they do not contain any information about the user's favorite programming language.

Citation check: insufficient-evidence. Chat claim present in the ask prompt: **False** (record: `runs/ask-20260928-211313-919.json`).

Assessment: Pass. The chat acknowledged "my favorite programming language is Rust" without a lookup; the separate ask answered "Insufficient evidence", and the claim does not appear in the ask prompt.

## M5: draft from notes, traceable

Expected: the draft looks up notes (it needs personal facts) and its facts match them, tagged [N#] or, if the model tags none, listed by the harness under the reply; "make that shorter" uses the conversation with no new lookup.

**you ›** Draft a 3-line LinkedIn post about my Ms. Pac-Man project.

_Harness routing: looked up notes — mentions wiki subject 'Ms. Pac-Man DQN'; 4 passages; 15.26 s._

**Wren ›**

> Here are a few options for a 3-line LinkedIn post, depending on the tone you want.
>
> **Option 1: Results-Focused (Good for technical audiences)**
>
> > Applied Deep Q-Learning to conquer Ms. Pac-Man! 🕹️
> > Successfully trained an agent, boosting the mean evaluation score by 84% (from 492 to 906).
> > Excited to share the journey of blending reinforcement learning with classic game AI. #ReinforcementLearning #DeepLearning
>
> **Option 2: Concise & Professional (Good for general networking)**
>
> > Diving into AI challenges with my Ms. Pac-Man DQN project.
> > Trained a DQN agent, achieving a significant performance uplift through careful hyperparameter tuning.
> > Always learning how complex algorithms translate into measurable results. #AI #MachineLearning
>
> **Option 3: A Bit More Casual (If you want to engage with other learners)**
>
> > Spent some time training an AI to play Ms. Pac-Man using DQN! 🟡
> > The biggest win? Seeing the score jump by over 400 points after training.
> > What are some cool RL projects others have worked on lately?
>
> Let me know if you want me to draft a longer version or tweak the tone on any of these.
>
> Notes used (not tagged claim by claim): [N1][N4] Ms. Pac-Man DQN; [N2] Deep Q-Network; [N3] Ms. Pac-Man DQN — Class 3 Assignment (original)

- [N1] `wiki/Projects/Ms. Pac-Man DQN.md:64-66` › Ms. Pac-Man DQN › Sources
- [N2] `wiki/Concepts/Deep Q-Network.md:31-31` › Deep Q-Network › Sources
- [N3] `raw/course-projects/pacman-dqn/README.md:3-9` › Ms. Pac-Man DQN — Class 3 Assignment
- [N4] `wiki/Projects/Ms. Pac-Man DQN.md:29-33` › Ms. Pac-Man DQN › Key facts › From course-projects/pacman-dqn/README.md

Citation check on [N#] tags: no-citations (so the harness listed the notes under the reply)

**you ›** make that shorter

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 10.45 s._

**Wren ›**

> Here are three even shorter options:
>
> **Option 1 (Ultra-Concise):**
> > Successfully trained a DQN agent to master Ms. Pac-Man. 🕹️
> > Achieved a substantial performance increase over baseline scores.
> > Excited about the intersection of RL and classic AI. #DeepLearning
>
> **Option 2 (Action-Oriented):**
> > Applied Deep Q-Learning to Ms. Pac-Man.
> > The agent learned to optimize its path for maximum score.
> > Great exercise in reinforcement learning implementation. #AI #DQN
>
> **Option 3 (Punchiest):**
> > Ms. Pac-Man + Deep Q-Learning = Smarter Agent. 🧠
> > Successfully trained a high-performing RL model.
> > Always pushing boundaries in game AI.

Chat log with exact messages: `runs/chat-20260928-211313-934.jsonl`

Assessment: Pass. The draft looked up notes because it names a wiki subject; every figure in it matches the notes (492 to 906, +84%, and "over 400 points" = +414 in N3). The model tagged no claims, so the harness listed the four notes under the reply (fix 15). "make that shorter" used the conversation with no new lookup and added no new facts.
