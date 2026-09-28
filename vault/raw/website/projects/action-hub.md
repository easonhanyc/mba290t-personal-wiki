---
title: "Action Hub — Ranked Alerts with Next Actions"
description: "A technical sales org had roughly 200 dashboards and no agreed place to start the day. This is the screen that replaced a manual sweep across five to ten of them."
summary: "A sales org with roughly 200 dashboards and no agreed starting point. The Action Hub ranks every open issue across a seller's accounts and puts the next action on each one — cutting time-to-insight 70% for 10,000+ sellers."
role: "Product owner · AWS Global Sales Strategy & Analytics"
period: "Jul 2023 – May 2026"
depth: "case-study"
org: "Amazon Web Services"
badges: ["0 → 1 at scale"]
live: false
tags: ["product", "ai", "analytics"]
metrics:
  - n: "70%"
    l: "less time-to-insight"
  - n: "10,000"
    l: "sellers served"
  - n: "$80B"
    l: "business supported"
links:
  prd: "/artifacts/prioritization-framework"
featured: true
order: 2
---
<aside class="note"><strong>Confidentiality note.</strong> Written at the level of detail already public on my resume. Internal system names, screenshots, dashboards and proprietary data are omitted; the diagram below is redrawn for this portfolio rather than captured from the product. Where an artifact appears it is a <strong>reconstruction</strong> built to show method, and is labelled as one.</aside>

> **The 30-second version.** A company-wide effort set out to replace AWS Sales's roughly 200 dashboards with a single source of truth, each org owning a chapter of it. I owned the technical sales chapter's **first tab** — the screen a seller lands on. The hard question was never what to display. It was what to put *first*, and what to say about it: an alert that names no next action moves the work rather than removing it. Time-to-insight fell **70%** for **10,000+ sellers**.

| | |
|---|---|
| **Problem** | Sellers had dashboards but no prescribed action; finding what was wrong took a manual sweep across 5–10 of them |
| **My role** | End-to-end: discovery, PRD, mockups, alert design and ranking model, roadmap prioritization, launch |
| **Outcome** | 70% reduction in time-to-insight · 10,000+ sellers |
| **Core decision** | Rank by **severity × account value**, and attach a destination to every alert — the alert is not the product, the redirect is |

---

## 1. The problem: two hundred dashboards and no front door

AWS Sales was not short of data. It was short of a *starting point*.

The org had accumulated on the order of two hundred dashboards. Each was individually reasonable and collectively unusable: to work out what needed attention today, a seller swept through five to ten of them, applying filters, and reconstructed a mental picture that the last person had also reconstructed an hour earlier.

Three costs fell out of that:

1. **The sweep was repeated work.** Every seller performed the same reconnaissance every morning, independently.
2. **It was inconsistent.** What you found depended on which dashboards you happened to check and how much time you had.
3. **The analytics function absorbed the gap** by fielding one-off data requests — a slow, unscalable substitute for a product. The size of that backlog was the clearest available evidence that self-service tooling was not self-service in practice.

A company-wide effort was set up to replace the sprawl with one source of truth, structured as a book: each org owns a chapter — technical sales, partner sales, revenue, attainment, marketing, usage, startups. My team owned the technical sales chapter, and the **Action Hub is its first tab**. The rest of the chapter carries account and pipeline detail and individual and leadership metrics. The first tab exists to answer one question before any of that: *what should I do today?*

**The reframe:** the bottleneck was never data *access*. Sellers already had access. It was the translation between "here is a number" and "here is what to do about it" — and that translation was being done by hand, by every seller, every morning.

That reframe is what turned a dashboard request into a product.

---

## 2. Discovery: what twenty interviews changed

I ran **20 user interviews** across segments before writing requirements, then scoped the build from a PRD and Figma prototypes. Two findings changed the design:

**Sellers didn't distrust the data; they distrusted their own reading of it.** The hesitation was never "is this number right," it was "am I looking at the right number." That pointed away from *more* visualisation and toward *fewer, ranked, prescribed* surfaces.

**The unit of work is an account, not a metric.** Dashboards were organised by metric — pipeline, coverage, attainment — because that is how an analytics org thinks. Sellers think in accounts. Reorganising around the seller's actual unit of work removed a translation step that was happening on every single visit.

The principle I'd carry into any PM role: **the org's internal information architecture leaks into the product, and users pay for it.**

---

## 3. How the product actually works

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 372" role="img" aria-labelledby="dg-t" xmlns="http://www.w3.org/2000/svg">
 <title id="dg-t">Alerts are detected per category, ranked by severity times account value, and each carries its own destination</title>
 <defs>
  <marker id="ah-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
  <g font-size="11.5" fill="var(--ink)">
   <rect x="10" y="14" width="132" height="44" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
   <text x="76" y="41">Revenue</text>
   <rect x="147" y="14" width="132" height="44" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
   <text x="213" y="41">Pipeline</text>
   <rect x="284" y="14" width="132" height="44" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
   <text x="350" y="41">Activity</text>
   <rect x="421" y="14" width="132" height="44" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
   <text x="487" y="41">Data hygiene</text>
   <rect x="558" y="14" width="132" height="44" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
   <text x="624" y="41">Development</text>
  </g>
  <path d="M350 58 L350 84" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#ah-ar)"/>
  <rect x="10" y="88" width="680" height="58" rx="7" fill="var(--tag-bg)" stroke="var(--border)"/>
  <text x="350" y="110" font-size="11.5" fill="var(--ink)">Threshold per metric &#8212; 15 alert types</text>
  <text x="350" y="131" font-size="10" fill="var(--ink-3)">usage anomaly &#8805; $20K WoW &#183; net usage &#8722;10% MoM &#183; stalled ARR &#8805; $100K &#183; partner ratio &lt; 75%</text>
  <path d="M350 146 L350 172" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#ah-ar)"/>
  <rect x="10" y="176" width="680" height="52" rx="7" fill="var(--surface)" stroke="var(--accent)"/>
  <text x="350" y="198" font-size="12.5" fill="var(--ink)">rank = severity weight (1&#8211;3) &#215; account YTD revenue</text>
  <text x="350" y="217" font-size="10" fill="var(--ink-3)">a medium alert on a large account outranks a high alert on a small one</text>
  <path d="M350 228 L350 254" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#ah-ar)"/>
  <g font-size="10.5" text-anchor="start">
   <rect x="10" y="258" width="680" height="30" rx="6" fill="var(--surface)" stroke="var(--border)"/>
   <text x="24" y="277" fill="var(--ink)">1 &#183; Net usage down 20% MoM</text>
   <text x="676" y="277" fill="var(--accent)" text-anchor="end">&#8594; revenue dashboard</text>
   <rect x="10" y="292" width="680" height="30" rx="6" fill="var(--surface)" stroke="var(--border)"/>
   <text x="24" y="311" fill="var(--ink)">2 &#183; Stalled opportunity, $1.4M ARR</text>
   <text x="676" y="311" fill="var(--accent)" text-anchor="end">&#8594; the opportunity record</text>
   <rect x="10" y="326" width="680" height="30" rx="6" fill="var(--surface)" stroke="var(--border)"/>
   <text x="24" y="345" fill="var(--ink)">3 &#183; Certification expiring in 45 days</text>
   <text x="676" y="345" fill="var(--accent)" text-anchor="end">&#8594; booking page</text>
  </g>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio. Top 50 alerts per person, scoped to their own accounts.</figcaption>
</figure>

**Detection is threshold-based, not modelled.** Fifteen alert types across five categories, each with an explicit cut-off on an existing metric: a week-over-week usage anomaly above $20K, net usage down more than 10% month-over-month, stalled technical-validation opportunities carrying over $100K ARR, a partner ratio under 75%, a certification inside 45 days of expiry, an account plan below 75% readiness.

Thresholds rather than a model was a deliberate choice. Every alert has to be explainable to the person receiving it in one sentence, because the first thing a seller does with an alert they don't understand is ignore it — and then ignore the next one.

**Ranking is severity multiplied by account value.** Each alert type carries a weight from 1 to 3; the multiplier is the account's year-to-date revenue. A month-over-month revenue decline weighs 3. A missing opportunity link on a feature request weighs 1.

That multiplication is the whole product judgment, and it has a consequence worth stating plainly: **a mid-severity alert on a major account outranks a high-severity alert on a small one.** That is correct for a sales org, and it is not what a pure severity sort would produce. A list ordered by severity alone sends your best sellers to your least important accounts.

Weighting also fixes the category problem structurally. Data hygiene matters, but it is never urgent — at weight 1 against revenue's 3, hygiene can only ever surface once the revenue problems on comparable accounts are exhausted. Nobody has to remember to deprioritise it.

**Every alert carries its own destination.** This is the part I would defend hardest. An alert that tells you something is wrong and leaves you to find the right dashboard has moved the search problem, not solved it. Each row resolves to the specific place the work happens — the revenue view, that opportunity record, the certification booking page. **The alert is not the product. The redirect is.**

**The list ends.** Top fifty per person. A ranked list with no bottom is just the dashboard sprawl again in a different shape.

**You only see your own book.** Alerts resolve through the territory and account registry, so each seller sees their own accounts and leadership sees their org. Without that, the ranked list is worse than useless — it is other people's work presented as yours.

---

## 4. Prioritization: a fixed date and more asks than fit

The hardest part was not the design. It was that the launch date was fixed and the requests substantially exceeded it.

I ran everything through P0/P1/P2 against three questions, in order:

1. **Does this change what a seller does today?** Anything that changed only what a seller *knew* went below the line. This is what "action-oriented" meant in practice, and it was the sharpest cut available.
2. **Does it work without a data-engineering dependency?** Features needing new upstream pipelines carried timeline risk owned by another team. Those were sequenced later, deliberately, so the launch date depended only on my own execution.
3. **Does it survive the seller's actual context?** Sellers are mobile, time-boxed and interrupted. A feature requiring a ten-minute focused session was mis-designed regardless of its value.

The second gate is the one I'd point to. It is tempting to treat an upstream dependency as someone else's risk to carry. It is not — it is your launch date, held by someone whose priorities you don't control.

→ *[Reconstructed prioritization framework](/artifacts/prioritization-framework) — the method, on generic example features*

---

## 5. What I'd do differently

- **I under-invested in instrumenting the "action taken" step.** Time-to-insight was measurable and improved 70% — measured as how long it took to locate the actual issue, before against after. Whether a seller then *acted* was much harder to observe, and I'd have designed for that measurement from the start instead of inferring it downstream.
- **I sequenced data-engineering dependencies out of v1 for schedule safety — correctly — but didn't push hard enough on the joint roadmap afterward.** Deferred dependencies have a way of staying deferred once v1 succeeds without them.
- **The weights were set from experience, not from evidence.** Severity weights came from judgment about what matters in a sales cycle. That was the right way to ship, and the wrong place to stay: every dismissal is a labelled example of a weight being wrong, and I did not capture them. A ranked list that never learns from being ignored is a ranked list that slowly stops being read.
