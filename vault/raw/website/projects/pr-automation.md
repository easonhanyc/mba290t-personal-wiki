---
title: "Pull-Request Automation"
description: "An OpenClaw skill that automates the ceremony between finishing a change and getting it reviewed — and deliberately stops there."
summary: "Getting a finished change into code review took eight mandatory steps and 30–60 minutes, none of it thinking. A skill built on Amazon's internal OpenClaw platform now does all eight, leaving about five minutes of genuine decisions — and stops precisely where a human reviewer starts."
role: "Builder and product owner · Amazon's internal OpenClaw platform"
period: "2023–2026"
depth: "project"
org: "Amazon Web Services"
badges: ["Agentic AI"]
live: false
tags: ["ai", "eng", "product"]
metrics:
  - n: "80%"
    l: "less manual processing time"
  - n: "5 min"
    l: "human input, from 30–60"
  - n: "8"
    l: "ceremony steps automated"
links: {}
featured: false
order: 3
---
<aside class="note"><strong>Confidentiality note.</strong> Written at the level of detail already public on my resume. Repository paths, build configuration and workflow specifics are omitted; the diagram is redrawn for this portfolio.</aside>

> **The 30-second version.** Shipping a change — SQL or Python — to the production repository meant eight mandatory steps before anyone could even look at it, and 30 to 60 minutes each time. None of that time was spent thinking. I built a skill on **Amazon's internal OpenClaw platform** that performs all eight, leaving about **five minutes** of actual decisions. It stops at the point a reviewer picks the change up, which is the only part of the sequence where a human was ever the point.

---

## 1. Eight steps between finishing and being reviewed

The change itself might take twenty minutes. Getting it to a place where a colleague could read it took longer than writing it:

1. Open the cloud desktop
2. Rebase against current main
3. Copy the code up from local
4. Authenticate and save it
5. Build in the beta environment
6. Run it in beta and check the output is right
7. Push the change as a new commit
8. Publish the review

Then a peer reviews it, and the data engineer on the team merges it to production.

Every one of those eight is mandatory, none is difficult, and none is where the work lives. It is ceremony — the tax between having done something and being able to show it to somebody.

Two things follow from that shape:

**The cost is per-change, so it taxes small changes hardest.** A one-line fix and a substantial rewrite carry identical overhead. That is a quiet incentive to batch changes into larger ones — which is the opposite of what you want, because large reviews are worse reviews.

**The step most likely to be skipped is step six.** Building and checking in beta is the one with no immediate consequence for skipping it, and it is the one you skip at 6pm on a Friday. The steps that protect you are always the steps under the most pressure.

## 2. What is automated, and where it stops

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 188" role="img" aria-labelledby="pr-t" xmlns="http://www.w3.org/2000/svg">
 <title id="pr-t">The skill automates the eight ceremony steps up to publishing the review; peer review and the merge to production stay human</title>
 <defs>
  <marker id="pr-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
  <rect x="8" y="40" width="86" height="48" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="51" y="62" font-size="10" fill="var(--ink)">Code</text>
  <text x="51" y="76" font-size="10" fill="var(--ink)">written</text>
  <path d="M94 64 L118 64" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#pr-ar)"/>
  <rect x="122" y="26" width="286" height="76" rx="8" fill="var(--tag-bg)" stroke="var(--accent)"/>
  <text x="265" y="20" font-size="10" fill="var(--accent)">automated &#8212; 8 steps</text>
  <text x="265" y="48" font-size="9.5" fill="var(--ink-2)">rebase &#183; copy up &#183; authenticate &#183; build in beta</text>
  <text x="265" y="64" font-size="9.5" fill="var(--ink-2)">run and validate &#183; push commit &#183; publish review</text>
  <text x="265" y="86" font-size="9.5" fill="var(--ink-3)">30&#8211;60 min &#8594; ~5 min of human input</text>
  <path d="M408 64 L432 64" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#pr-ar)"/>
  <rect x="436" y="40" width="96" height="48" rx="7" fill="var(--surface)" stroke="var(--gold)"/>
  <text x="484" y="62" font-size="10" fill="var(--ink)">Peer</text>
  <text x="484" y="76" font-size="10" fill="var(--ink)">review</text>
  <path d="M532 64 L556 64" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#pr-ar)"/>
  <rect x="560" y="40" width="90" height="48" rx="7" fill="var(--surface)" stroke="var(--gold)"/>
  <text x="605" y="62" font-size="10" fill="var(--ink)">Engineer</text>
  <text x="605" y="76" font-size="10" fill="var(--ink)">merges</text>
  <path d="M650 64 L676 64" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#pr-ar)"/>
  <text x="545" y="112" font-size="9.5" fill="var(--gold)">unchanged &#8212; where judgment lives</text>
  <text x="350" y="146" font-size="10.5" fill="var(--ink-2)">The skill ends at &#8220;published for review&#8221;. It does not review,</text>
  <text x="350" y="162" font-size="10.5" fill="var(--ink-2)">and it does not merge.</text>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio. Internal platform and repository details omitted.</figcaption>
</figure>

The skill covers the whole span from opening the cloud desktop to publishing the review. It does not review the change, and it does not merge it.

That boundary is the design, and it is worth stating as a rule: **automate up to the point where judgment starts, and stop there sharply.** Not "stop where the model gets unreliable" — stop where a human being was the reason the step existed. A peer reads the change because somebody other than the author should look at it. A data engineer merges because production is their responsibility. Neither of those is overhead that happens to be manual; both are the point.

Automating *toward* the reviewer rather than *past* them also means the failure mode is contained. The worst thing the skill can do is publish a bad review — which a reviewer then reads, disagrees with, and rejects. That is the system working.

## 3. The five minutes that stay human

What remains is not leftover friction. It is the set of things the automation genuinely cannot infer, and naming them precisely is what made it possible to automate everything else:

- **Where the file is locally.** No safe default; guessing wrong pushes the wrong change.
- **What configuration applies on this push.** Depends on what the change is for.
- **If there is a DDL change, which folder it belongs in.** Schema changes are placed by convention, and convention is a judgment about what the change *means*, not what it contains.

Each of these is a question with a right answer that only the author holds. Everything else in the sequence was a step with exactly one correct execution, repeated identically every time — which is the definition of work worth automating.

**The useful test is not "can this be automated" but "does this step have more than one correct outcome."** If it does, a person decides. If it doesn't, nobody should be spending thirty minutes a week on it.

## 4. Validation stops being skippable

The skill builds the change in the beta environment, runs it, and validates the output before it pushes anything. It also handles the errors that come back rather than stopping at the first one.

This is the part I would argue is more valuable than the time saved, even though the time saved is what the number measures.

Step six — build it and check the result — was always the correct thing to do and always the first thing to go under deadline pressure. Making it automatic doesn't just make it faster; it makes it **unconditional**. The check now happens on the 6pm Friday change exactly as it happens on the Tuesday morning one.

Reliability improvements that depend on people being disciplined degrade precisely when the system is under the most stress. Moving the check into the path removes the discipline requirement entirely.

## 5. Why the 80% understates it

Thirty to sixty minutes down to about five is the headline, and it is a per-change number.

But the second-order effect is the one worth watching. When overhead per change is high, the rational response is to batch — bundle several changes into one review so the tax is paid once. Large reviews get worse scrutiny, because reviewer attention does not scale linearly with diff size, and problems hide in volume.

**Cutting per-change overhead removes the incentive to batch.** Smaller, more frequent reviews are easier to read, easier to reason about, and easier to revert. None of that shows up in "80% less manual processing time," and all of it follows from it.
