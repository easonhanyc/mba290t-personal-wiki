---
title: Prioritization Framework
type: concept
summary: A four-gate method for cutting a roadmap, written up as a reconstruction of the one Eason used on the AWS Sales insights platform (the Action Hub); the example features in the write-up are generic, invented for the portfolio.
sources:
- path: raw/website/artifacts/prioritization-framework.md
  source_id: website-artifacts-prioritization-framework-ba375a97
  sha256: ba375a97db9f4c7cc268f43a5c9eb56b80052076469ed15463ea25f38c41d004
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-28T21:06:58'
reviewed: true
previous_names:
- Prioritization Framework Method
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-28T21:29
---

# Prioritization Framework

A four-gate method for cutting a roadmap, written up as a reconstruction of the one Eason used on the AWS Sales insights platform (the Action Hub); the example features in the write-up are generic, invented for the portfolio. A feature that fails an early gate is never scored, so the room gets a decision instead of an arguable score.

## Key facts
- The write-up's starting claim: most prioritization frameworks fail in practice because they produce a score when the room needs a decision, and scores are easy to argue with. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md]])
- The four gates are applied in order, each cheaper to evaluate than the next, so a feature that fails early skips the expensive analysis. ([[raw/website/artifacts/prioritization-framework#The gates, in order|website/artifacts/prioritization-framework.md › The gates, in order]])
- Gate 1 asks whether a feature changes what the user does or only what they know; the write-up calls it the sharpest cut for an analytics product because it can be answered without data. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md › Gate 1 — Does this change what the user *does*, or only what they *know*?]])
- Features that change behavior go above the line; features that only change knowledge go below it, unless they feed a behavior-changing feature. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md › Gate 1 — Does this change what the user *does*, or only what they *know*?]])
- Gate 2 asks whether shipping depends on a team the author does not control; a dependency is a reason to sequence the feature later and raise the dependency as a joint roadmap item now, not to kill it. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md › Gate 2 — Does shipping this depend on a team I don't control?]])
- Gate 3 checks the user's real context (uninterrupted time, device and posture, what is already open): a feature that needs a ten-minute focused session is mis-designed for an interrupted user, however much value it would deliver. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md › Gate 3 — Does it survive the user's real context?]])
- Gate 4 scores reach × impact ÷ effort only for what survived the first three gates, because only then is the list comparable enough for scores to mean something. ([[raw/website/artifacts/prioritization-framework|website/artifacts/prioritization-framework.md › Gate 4 — Only now, score reach × impact ÷ effort]])
- Three additions that prevent re-litigation of a ranked list are publishing the below-the-line list, stating the gate each cut item failed, and naming what would change the ranking. ([[raw/website/artifacts/prioritization-framework#What I make explicit alongside the ranked list|website/artifacts/prioritization-framework.md › What I make explicit alongside the ranked list]])
- The rule the write-up says generalizes: a request that shows up three times is a missing feature, so repeated asks should be promoted into the roadmap instead of answered one by one. ([[raw/website/artifacts/prioritization-framework#The one that generalizes|website/artifacts/prioritization-framework.md › The one that generalizes]])

## Related notes
- [[Action Hub]] — The write-up says this is the method used on the AWS Sales insights platform, the Action Hub; the Action Hub page links to it as the framework behind its PRD.
- [[Amazon Web Services]] — The method comes from this role, where it was used to cut the insights platform's roadmap.

## Sources
- [[raw/website/artifacts/prioritization-framework|Personal website - artifacts: Prioritization framework]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/artifacts/prioritization-framework.md)
