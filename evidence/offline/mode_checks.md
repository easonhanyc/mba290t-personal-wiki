# Mode-boundary checks

Label `offline`, 2026-09-28T14:12:39. Execution: local (llama.cpp on 127.0.0.1), model `gemma-4-e4b-it-qat-q4_0`; internet: **offline**.

## M1: casual chat, capabilities

Expected: accurate capabilities and a suggested starting point; no notes lookup, no citations, no insufficient-evidence refusal.

**you ›** what can you help me with?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 16.06 s._

**Wren ›**

> I'm here to help you manage your workflow, Eason. Think of me as your Chief of Staff running off your laptop.
>
> I can assist with:
>
> *   **Drafting and Refining:** Brainstorming, drafting, and rewriting emails, reports, or presentation content.
> *   **Organization:** Keeping track of projects, notes, and action items based on what you tell me or what's in the wiki.
> *   **Information Retrieval:** Pulling specific details from your stored notes using commands like `/notes` or `wiki ask`.
> *   **Planning:** Helping you outline next steps for assignments or work.
>
> Basically, anything that requires organization, drafting, or accessing the information you've given me.
>
> What's on your mind right now?

**you ›** what can we do?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 12.16 s._

**Wren ›**

> We can tackle whatever is currently taking up space in your head. To give you a concrete suggestion, I need a little context.
>
> Are you working on:
>
> *   **A specific assignment** (e.g., for MBA 290T)?
> *   **A work project**?
> *   **General planning** for the week?
> *   **Just need to clear some mental clutter**?
>
> If you tell me the domain, I can offer a few immediate options. Otherwise, let me know if you want to start drafting something or reviewing some notes.

Chat log with exact messages: `runs/chat-20260928-141328-709.jsonl`

Assessment: Pass. Both capability questions were answered from the persona with no notes lookup, no citations and no insufficient-evidence refusal, and each ends with a starting point. The capability list matches the harness (drafting, planning, /notes lookups).

## M2: conversational follow-up

Expected: second answer is a shorter version of the first plan (uses conversation history).

**you ›** Draft a short plan for my week: I need to finish Assignment 4 and prep for PM internship applications.

_Harness routing: no notes lookup — drafting/planning from what you said: no personal facts needed; 19.43 s._

**Wren ›**

> Here is a draft plan for the week. I've kept it high-level; we can drill down on specific tasks once you confirm the priorities.
>
> **Focus Areas:**
> 1.  **Assignment 4 Completion:** Dedicate focused time to wrapping this up.
> 2.  **PM Internship Applications:** Systematically build out application materials and target roles.
>
> **Suggested Breakdown:**
>
> *   **Mon/Tues:** Deep work on Assignment 4. Block out dedicated time slots.
> *   **Wed:** Review and refine core application materials (e.g., resume, PM case study examples).
> *   **Thurs:** Target and apply to 2-3 specific PM roles.
> *   **Fri:** Final review of Assignment 4; outline next steps for applications/interview prep.
>
> Let me know if this structure works, or if you want me to flesh out the Assignment 4 milestones or suggest a structure for your application targeting.

**you ›** make that shorter

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 7.24 s._

**Wren ›**

> Here is a tighter version:
>
> *   **Mon-Tues:** Finish Assignment 4.
> *   **Wed:** Polish PM application materials.
> *   **Thurs:** Apply to target PM roles.
> *   **Fri:** Review/Next steps.
>
> Does this work, or should I prioritize one over the other?

Chat log with exact messages: `runs/chat-20260928-141356-948.jsonl`

Assessment: Pass. The week plan was drafted without a notes lookup (nothing personal was needed), and "make that shorter" produced a condensed version of the same plan from the conversation history. This re-runs the check that failed in the dry run (fix 7 in evidence/changes.md).

## M3: raw search

Expected: original passages with source paths; zero model calls; also works with the Gemma server stopped.

Gemma server running during this search: **False**. Model calls: **0**. Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion). Time: 0.023 s.

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

Assessment: Pass. With the Gemma server stopped, search returned six original passages with paths and line numbers and made zero model calls.

## M4: ask ignores chat history

Expected: ask reports insufficient evidence; the saved ask prompt contains no chat text.

**you ›** By the way, my favorite programming language is Rust.

_Harness routing: no notes lookup — model router decided no notes needed; 11.25 s._

**Wren ›**

> Got it. Rust. I'll keep that in mind.
>
> Do you need me to look for any resources, articles, or potential projects related to Rust for your work or studies?

Chat log with exact messages: `runs/chat-20260928-141427-028.jsonl`

Then, separately: `wiki ask "What is my favorite programming language?"`

> Insufficient evidence: The provided passages describe course materials, project structures, and technical concepts related to AI and programming, but they do not state what the user's favorite programming language is.

Citation check: insufficient-evidence. Chat claim present in the ask prompt: **False** (record: `runs/ask-20260928-141458-515.json`).

Assessment: Pass. The chat acknowledged "my favorite programming language is Rust" without a lookup; the separate ask answered "Insufficient evidence", and the claim does not appear anywhere in the ask prompt.
