---
title: "GenAI Target Setting"
description: "Setting the first-ever annual target for a business with almost no history — by forecasting the leading indicator instead of the goal."
summary: "The first year AWS carried a GenAI goal, the metric being targeted had barely existed twelve months earlier. Forecasting it directly was impossible, so the model forecast a leading indicator that did have history and converted through it — then shipped with a quarterly mechanism to correct itself."
role: "Analytics and target-setting methodology · AWS Global Sales Strategy & Analytics"
period: "2024"
depth: "project"
org: "Amazon Web Services"
badges: ["Forecasting"]
live: false
tags: ["analytics", "ai", "product"]
metrics:
  - n: "55,000"
    l: "data points"
  - n: "4"
    l: "scenario simulations"
  - n: "3-month"
    l: "cycle-time lag"
links: {}
featured: false
order: 4
---
<aside class="note"><strong>Confidentiality note.</strong> Written at the level of detail already public on my resume. No actual targets, conversion rates, pipeline volumes or regional figures appear here — those are live commercial metrics. What is described is the method and the reasoning, which is the part that generalises.</aside>

> **The 30-second version.** 2024 was the first year AWS Sales carried a Generative AI goal. The problem: the metric being targeted had barely existed a year earlier, and had grown by roughly two orders of magnitude across the baseline year. There was no stable series to regress on. I built the target-setting model across **55,000 data points and four scenario simulations**, and the decision that made it work was **not forecasting the target metric at all**.

---

## 1. How a goal becomes a number

The AWS Sales technical org — solutions architects and customer solutions managers — carries
annual goals every year, drawn from whatever leadership has decided matters most that cycle.
**2024 was the first year Generative AI was one of them.**

That makes target-setting an analytics problem before it is a planning one. The sequence runs:
construct the goal with the VP and the goal's business owners at the start of the year, derive
the number, and then **release it down to every team and every individual contributor**.

That last step is what raises the stakes. A target here is not a slide in a planning deck — it
becomes the number a few thousand individual people are measured against for twelve months.
Getting it wrong in either direction has a cost: too high and you have demotivated an entire
org against a category nobody yet understands; too low and you have under-invested in the
fastest-moving thing in the business.

## 2. Why the obvious approach fails

You set next year's target by looking at this year's trend. That assumes a trend exists.

For a brand-new category it doesn't. Across the baseline year the metric ran at effectively nothing for the first several months, then climbed steeply once the category took off. Fitting a line through that series gives you a number, and the number is meaningless: half the observations are noise around zero, and the slope you extract is dominated by whichever months you happen to include.

Worse, it fails in a specific and expensive direction. A line fitted through an exponential take-off **under-predicts if you weight the early months and over-predicts if you weight the late ones** — and there is no principled basis for choosing, because the thing driving the curve is category adoption, not anything the sales org controls.

So the first real decision was to stop trying.

## 3. Forecast something that does have history

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 196" role="img" aria-labelledby="g1-t" xmlns="http://www.w3.org/2000/svg">
 <title id="g1-t">Pipeline creation is forecast by linear trend, then converted through tech attach and win rate, landing three months later as the target</title>
 <defs>
  <marker id="g1-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
  <rect x="8" y="34" width="150" height="52" rx="7" fill="var(--surface)" stroke="var(--accent)"/>
  <text x="83" y="57" font-size="11" fill="var(--ink)">Pipeline created</text>
  <text x="83" y="73" font-size="9.5" fill="var(--ink-3)">has real history</text>
  <path d="M158 60 L196 60" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#g1-ar)"/>
  <rect x="200" y="34" width="140" height="52" rx="7" fill="var(--tag-bg)" stroke="var(--border)"/>
  <text x="270" y="57" font-size="11" fill="var(--ink)">Linear trend</text>
  <text x="270" y="73" font-size="9.5" fill="var(--ink-3)">least squares</text>
  <path d="M340 60 L378 60" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#g1-ar)"/>
  <rect x="382" y="34" width="140" height="52" rx="7" fill="var(--tag-bg)" stroke="var(--border)"/>
  <text x="452" y="52" font-size="11" fill="var(--ink)">&#215; tech attach</text>
  <text x="452" y="69" font-size="11" fill="var(--ink)">&#215; win rate</text>
  <text x="452" y="82" font-size="9.8" fill="var(--ink-3)">per region</text>
  <path d="M522 60 L560 60" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#g1-ar)"/>
  <rect x="564" y="34" width="128" height="52" rx="7" fill="var(--surface)" stroke="var(--accent)"/>
  <text x="628" y="57" font-size="11" fill="var(--ink)">Target</text>
  <text x="628" y="73" font-size="9.5" fill="var(--ink-3)">month N+3</text>
  <path d="M83 92 L83 118 L628 118 L628 96" stroke="var(--gold)" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="355" y="134" font-size="10" fill="var(--gold)">3-month cycle time &#8212; pipeline created in month N closes in month N+3</text>
  <text x="355" y="166" font-size="10.5" fill="var(--ink-2)">Forecast the leading indicator that has history,</text>
  <text x="355" y="182" font-size="10.5" fill="var(--ink-2)">not the goal metric that has none.</text>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio. Conversion rates and volumes omitted.</figcaption>
</figure>

Pipeline creation had been running long enough to have a real series. So the model forecasts **pipeline**, then converts it into the goal metric:

1. **Forecast pipeline creation.** Least-squares linear trend, fitted only on the months where the category was genuinely active — six months of actuals — and projected forward by region.
2. **Apply a technical-attach rate.** The share of created pipeline that becomes an attached, launched opportunity.
3. **Apply a win rate.** The share of that which closes.
4. **Lag by cycle time.** Median open-to-close for opportunities in this category was about three months, so pipeline created in month N lands in month N+3.

Target for a month is therefore *pipeline created three months earlier × attach × win*, computed per region.

## 4. The judgment calls inside that

**Which months feed the trend.** Only the window where the category was actually active. Including the dead months earlier in the year would have dragged the intercept down and flattened the slope — mathematically fine, commercially wrong.

**Which months feed the rates.** Attach and win rates came from the *later* months only — the first period with enough launches per month to compute a rate that wasn't noise. A conversion rate derived from a handful of opportunities is a number with no information in it, and it would have propagated straight into every regional quota.

Note that these two windows are deliberately different. The trend wants the longest honest series; the rates want the densest one. Using one window for both would have compromised whichever it was wrong for.

**Per region, not global.** Attach and win rates differ materially between regions. A single blended rate would have been easier to defend and would have quietly misallocated quota — over-targeting regions that convert poorly and under-targeting the ones that convert well. This is the step that actually determines what each region is asked to carry, which makes it the step people argue about.

**Rates held flat, on purpose.** The model assumes conversion doesn't improve over the year, with an explicit note that the estimate should be revised as enablement mechanisms take effect. That is a conservative assumption and a knowingly wrong one — improvement was the whole point of the programme. It was the right default because a target built on assumed improvement is a target that blames the field for a forecasting choice.

## 5. What the scenarios are for

Four scenario simulations, run as sensitivity analysis across the model's assumptions.

The point is not to produce a better single number. It is that a point forecast for a category with no history **invites false precision** — and the conversation it produces is an argument about whether the number is right, which nobody can settle.

Scenarios change the question. Instead of "is 'X' correct," the conversation becomes **"which set of assumptions is leadership willing to bet the year on"** — which is answerable, and which surfaces the disagreement where it actually lives. That is a materially better input to target-setting than a single figure with a confidence interval nobody believes.

→ *[Reconstructed metric tree](/artifacts/metric-tree) — the decomposition method, on a generic example*

## 6. The part that mattered most: planning to be wrong

A target for a category with no history **will** be wrong. Not might — will. The honest response is not a better model; it is to ship the number alongside the mechanism for correcting it.

So the deliverable was not the target. It was the target plus a **quarterly review cadence**: measure actual conversion against the assumed rates, measure actual pipeline against the trend, and adjust while there is still year left to adjust in.

This is the thing I'd argue for in any planning conversation. **An annual number set once in February and defended for eleven months is a worse instrument than a slightly worse number that gets corrected in April.** The first optimises for the appearance of rigour. The second optimises for the org steering correctly.
