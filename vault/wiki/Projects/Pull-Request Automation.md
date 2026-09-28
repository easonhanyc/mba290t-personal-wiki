---
title: Pull-Request Automation
type: project
summary: This project involved building a skill on Amazon's internal OpenClaw platform to automate the mandatory steps between finishing a code change and getting it reviewed.
sources:
- path: raw/website/projects/pr-automation.md
  source_id: website-projects-pr-automation-cfba0828
  sha256: cfba08280fdab5cf6c1693725221feb4733ff71ac15bc0451dd50db0b7eb3831
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:57:36'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-27T01:06
---

# Pull-Request Automation

This project involved building a skill on Amazon's internal OpenClaw platform to automate the mandatory steps between finishing a code change and getting it reviewed. The automation reduced the manual processing time by 80%, leaving only about five minutes of human decision-making.

## Key facts
- The skill automates the eight ceremony steps up to publishing the review; peer review and the merge to production stay human. ([[raw/website/projects/pr-automation#2. What is automated, and where it stops|website/projects/pr-automation.md › 2. What is automated, and where it stops]])
- Getting a finished change into code review took eight mandatory steps and 30–60 minutes, none of it thinking. ([[raw/website/projects/pr-automation|website/projects/pr-automation.md]])
- The skill covers the whole span from opening the cloud desktop to publishing the review. ([[raw/website/projects/pr-automation#2. What is automated, and where it stops|website/projects/pr-automation.md › 2. What is automated, and where it stops]])
- The useful test is not "can this be automated" but "does this step have more than one correct outcome." ([[raw/website/projects/pr-automation#3. The five minutes that stay human|website/projects/pr-automation.md › 3. The five minutes that stay human]])
- The skill builds the change in the beta environment, runs it, and validates the output before it pushes anything. ([[raw/website/projects/pr-automation#4. Validation stops being skippable|website/projects/pr-automation.md › 4. Validation stops being skippable]])
- Cutting per-change overhead removes the incentive to batch. ([[raw/website/projects/pr-automation#5. Why the 80% understates it|website/projects/pr-automation.md › 5. Why the 80% understates it]])

## Related notes
- [[Amazon Web Services]] — Built in this role on Amazon's internal OpenClaw platform.
- [[Allowlist Data Access App]] — Another internal tool from the same AWS role.

## Sources
- [[raw/website/projects/pr-automation|Personal website - projects: Pull-Request Automation]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/pr-automation.md)
