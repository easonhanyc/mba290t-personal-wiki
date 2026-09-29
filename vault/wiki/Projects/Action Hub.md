---
title: Action Hub
type: project
summary: Action Hub was built to replace a manual sweep across roughly 200 dashboards for a technical sales organization.
sources:
- path: raw/website/projects/action-hub.md
  source_id: website-projects-action-hub-c6c9d5e9
  sha256: c6c9d5e9923905957c0f62ed78fd7650a5859ddaa918013f86ce6aec7f83342a
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T01:06:10'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-28T21:29
---

# Action Hub

Action Hub was built to replace a manual sweep across roughly 200 dashboards for a technical sales organization. It ranks every open issue across a seller's accounts and puts the next action on each one, cutting time-to-insight by 70% for over 10,000 sellers.

## Key facts
- A technical sales org had roughly 200 dashboards and no agreed place to start the day. ([[raw/website/projects/action-hub|website/projects/action-hub.md › front matter]])
- The Action Hub ranks every open issue across a seller's accounts and puts the next action on each one — cutting time-to-insight 70% for 10,000+ sellers. ([[raw/website/projects/action-hub|website/projects/action-hub.md › front matter]])
- Sellers had dashboards but no prescribed action; finding what was wrong took a manual sweep across 5–10 of them. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 1. The problem: two hundred dashboards and no front door]])
- A company-wide effort was set up to replace the sprawl with one source of truth, structured as a book: each org owns a chapter — technical sales, partner sales, revenue, attainment, marketing, usage, startups. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 1. The problem: two hundred dashboards and no front door]])
- 20 user interviews across segments were run before writing requirements; the build was then scoped from a PRD and Figma prototypes. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 2. Discovery: what twenty interviews changed]])
- Sellers didn't distrust the data; they distrusted their own reading of it. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 2. Discovery: what twenty interviews changed]])
- Detection is threshold-based, not modelled. ([[raw/website/projects/action-hub#3. How the product actually works|website/projects/action-hub.md › 3. How the product actually works]])
- Ranking is severity multiplied by account value. ([[raw/website/projects/action-hub#3. How the product actually works|website/projects/action-hub.md › 3. How the product actually works]])
- Every alert carries its own destination. ([[raw/website/projects/action-hub#3. How the product actually works|website/projects/action-hub.md › 3. How the product actually works]])
- The hardest part was not the design. It was that the launch date was fixed and the requests substantially exceeded it. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 4. Prioritization: a fixed date and more asks than fit]])
- When scope had to be cut, requests that changed only what a seller knew went below the line. ([[raw/website/projects/action-hub|website/projects/action-hub.md › 4. Prioritization: a fixed date and more asks than fit]])
- A stated lesson: instrumenting the 'action taken' step was under-invested. ([[raw/website/projects/action-hub#5. What I'd do differently|website/projects/action-hub.md › 5. What I'd do differently]])

## Related notes
- [[Amazon Web Services]] — Built in this role at AWS Global Sales Strategy & Analytics.
- [[Allowlist Data Access App]] — Both scope what each seller may see through the territory and account assignments.
- [[Job Search Agent]] — Both rank a long list and cap it on purpose: fifty alerts per seller here, two roles per company there.
- [[Prioritization Framework]] — The four-gate method used to cut this product's roadmap; this page links to it as the framework behind the PRD.

## Sources
- [[raw/website/projects/action-hub|Personal website - projects: Action Hub — Ranked Alerts with Next Actions]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/action-hub.md)
