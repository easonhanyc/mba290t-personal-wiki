---
title: "Prioritization framework"
description: "Four ordered gates for cutting a roadmap."
kind: "Method"
related: "action-hub"
order: 3
---

> **This is a reconstruction.** The method is the one I used on the [AWS Sales insights platform](/work/action-hub); the example features below are generic, invented for this portfolio. No internal roadmap content appears here.

Most prioritization frameworks fail in practice for the same reason: they produce a *score* when what the room actually needs is a *decision*, and scores are easy to argue with. What follows is what I use instead — a small number of ordered gates, where a feature that fails an early gate doesn't get scored at all.

---

## The gates, in order

Order matters. Each gate is cheaper to evaluate than the one after it, so failing early saves the expensive analysis.

### Gate 1 — Does this change what the user *does*, or only what they *know*?

The single sharpest cut available on an analytics or insights product, and the one that survives contact with stakeholders best — because it's answerable without data.

| | Changes behavior | Only changes knowledge |
|---|---|---|
| **Example** | "Flag the three accounts most at risk this week" | "Add a year-over-year comparison chart" |
| **Disposition** | Above the line | Below, unless it feeds something in the left column |

The uncomfortable version of this gate: **a large share of requested dashboard features fail it.** They're requested sincerely, and they'd be used, but nobody acts differently because of them. Naming that out loud is most of the value.

### Gate 2 — Does shipping this depend on a team I don't control?

Not a reason to kill a feature. It's a reason to *sequence* it deliberately rather than accidentally.

- **No external dependency** → eligible for v1; ship date depends only on my own execution.
- **External dependency** → sequenced later, with the dependency raised as a joint roadmap item *now*, not when it becomes blocking.

The failure mode this prevents: a v1 whose launch date is quietly hostage to another team's priorities, discovered two weeks before the deadline.

### Gate 3 — Does it survive the user's real context?

Every feature implicitly assumes a usage context. Make it explicit and check it:

- How much uninterrupted time does this need? (Sellers are time-boxed and interrupted.)
- What device, and in what posture — desk, phone, between meetings?
- What does the user already have open?

A feature requiring a ten-minute focused session is mis-designed for an interrupted user *regardless of how much value it would deliver in that session.* This gate kills otherwise-good ideas, which is how you know it's doing work.

### Gate 4 — Only now, score reach × impact ÷ effort

Whatever survives the first three gates is largely comparable, which is exactly the condition under which scoring is actually meaningful. Scoring an incomparable list is theater.

---

## What I make explicit alongside the ranked list

A ranked list alone reliably gets re-litigated. Three additions that prevent that:

**1. The below-the-line list, published.** Stakeholders accept "not now" far better than silence. An idea that visibly survives in a "later" column doesn't need to be re-argued every review.

**2. The gate each cut item failed.** "Below the line" invites debate; "this fails Gate 1 — nobody acts differently" is a specific claim someone can actually refute with evidence. Specific disagreement is productive; vague disagreement isn't.

**3. What would change the ranking.** Naming the trigger in advance ("if this request recurs three more times, it becomes a roadmap item") converts a recurring argument into a standing rule.

---

## The one that generalizes

> **A request that shows up three times is a missing feature wearing a disguise.**

Intake is where this gets decided. A process that treats every request as a one-off spends its life re-answering the same question; one that separates *one-off asks* from *repeated asks*, and promotes the second kind into the roadmap, stops paying that cost twice. The recurring request is not a support burden — it is a feature you have not written down yet.

---
