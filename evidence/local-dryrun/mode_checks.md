# Mode-boundary checks

Label `local-dryrun`, 2026-09-27T01:07:14. Execution: local (llama.cpp on 127.0.0.1), model `gemma-4-e4b-it-qat-q4_0`; internet: **ONLINE**.

## M1: casual chat, capabilities

Expected: accurate capabilities and a suggested starting point; no notes lookup, no citations, no insufficient-evidence refusal.

**you ›** what can you help me with?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 22.62 s._

**Wren ›**

> I'm here to help you manage your work, whether that's brainstorming, drafting, or organizing your thoughts. Think of me as a sounding board for your projects and studies at Haas.
>
> Specifically, I can:
>
> *   **Organize and Draft:** Help you structure arguments, draft emails, or refine presentations.
> *   **Recall Information:** Access your notes on projects, coursework, and other relevant topics using commands like `/notes <topic>`.
> *   **Brainstorm:** Work through complex problems or generate ideas for your work.
>
> What's on your mind right now? A specific project, a tough reading, or just a general need to get organized?

**you ›** what can we do?

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 20.15 s._

**Wren ›**

> We can tackle whatever needs organizing or drafting today. Since I only know what you tell me or what's in your notes, the possibilities depend on your current priorities.
>
> Here are a few things we could do:
>
> *   **Review a Project:** If you have a specific project, we can outline it, critique a draft, or brainstorm next steps.
> *   **Prep for Class:** We can go over concepts from MBA 290T or other courses if you want to test your understanding or structure study notes.
> *   **Draft Communications:** Need to write a difficult email or a concise update for a stakeholder? I can draft that.
> *   **Organize Thoughts:** If you're feeling scattered, we can use a free-form chat to dump ideas, and I can help structure them into actionable points.
>
> What feels most pressing right now?

Chat log with exact messages: `runs/chat-20260927-010923-419.jsonl`

Assessment: Pass. Capabilities explained with no notes lookup.

## M2: conversational follow-up

Expected: second answer is a shorter version of the first plan (uses conversation history).

**you ›** Draft a short plan for my week: I need to finish Assignment 4 and prep for PM internship applications.

_Harness routing: looked up notes — mentions wiki subject 'TikTok Internship'; 4 passages; 30.07 s._

**Wren ›**

> Here is a draft plan to tackle Assignment 4 and your PM internship prep.
>
> **Immediate Focus:**
> *   **Assignment 4:** This is due next week, Tuesday, 9/29 [N1]. Need to prioritize finishing this build.
> *   **Internship Prep:** Leveraging your Job Search Agent [N2], we can streamline the application pipeline.
>
> **Suggested Weekly Plan:**
>
> *   **Daily (30-60 min):** Run/review the Job Search Agent [N2]. Focus on analyzing the quality of the roles it pulls, not just the volume.
> *   **Mid-Week Focus (Deep Work):** Dedicate a solid block of time specifically to finishing the implementation for Assignment 4 [N1].
> *   **Application Prep:** Once Assignment 4 is locked down, pivot to tailoring materials. We can use the roles found by your agent to practice drafting targeted outreach or custom cover letters.
>
> How does that look? We can drill down into a specific time block for Assignment 4 if you want to start there.

- [N1] `raw/course/syllabus.html:498-536` › MBA 290T: Fundamental of Agentic AI › Graded Assignments
- [N2] `wiki/Projects/Job Search Agent.md:18-18` › Job Search Agent
- [N3] `raw/course/syllabus.html:413-418` › MBA 290T: Fundamental of Agentic AI › Class Schedule
- [N4] `raw/website/projects/job-search-agent.md:1-25` › Properties

Citation check on [N#] tags: citation-problems

**you ›** make that shorter

_Harness routing: no notes lookup — casual, capability or edit request: answered from the conversation; 9.37 s._

**Wren ›**

> Here is the condensed version:
>
> *   **Mon-Wed:** Finish Assignment 4 [N1].
> *   **Thurs-Fri:** Focus on PM internship applications using the Job Search Agent [N2].
> *   **Daily:** Quick review of agent output.
>
> Ready to assign specific tasks for Monday?

Chat log with exact messages: `runs/chat-20260927-011006-237.jsonl`

Assessment: Failed as a routing check (kept as evidence). The planning request looked up notes because the word "internship" matched the note "TikTok Internship"; the resulting plan was sensible and its one note-based claim (Assignment 4 due 9/29) was cited, but the lookup reason was wrong. Fixed (fix 7) and re-run offline.

## M3: raw search

Expected: original passages with source paths; zero model calls; also works with the Gemma server stopped.

Gemma server running during this search: **False**. Model calls: **0**. Method: hybrid (BM25 + EmbeddingGemma, reciprocal-rank fusion). Time: 0.031 s.

| # | Passage | Section |
|---|---|---|
| 1 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:52-83` | How this app works › 3. The ownership rule › Layer 2 — Row Level Security filters every statement |
| 2 | `raw/course-projects/secure-networking-tracker/docs/how-it-works.md:85-89` | How this app works › 3. The ownership rule › Layer 2 — Row Level Security filters every statement |
| 3 | `wiki/Projects/Secure Networking Tracker.md:39-46` | Secure Networking Tracker › Key facts › From course-projects/secure-networking-tracker/docs/how-it-works.md |
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

Assessment: Pass. Search returned passages with the Gemma server stopped and zero model calls.

## M4: ask ignores chat history

Expected: ask reports insufficient evidence; the saved ask prompt contains no chat text.

**you ›** By the way, my favorite programming language is Rust.

_Harness routing: no notes lookup — model router decided no notes needed; 11.0 s._

**Wren ›**

> Got it. Rust. I'll keep that in mind.
>
> Anything specific you're working on with it, or should I just file that away for now?

Chat log with exact messages: `runs/chat-20260927-011049-516.jsonl`

Then, separately: `wiki ask "What is my favorite programming language?"`

> Insufficient evidence: The provided passages detail course material, project structures, and evaluation methods for a course, but they do not contain any information about the user's favorite programming language.

Citation check: insufficient-evidence. Chat claim present in the ask prompt: **False** (record: `runs/ask-20260927-011119-233.json`).

Assessment: Pass. Insufficient evidence; the chat claim was not in the ask prompt.
