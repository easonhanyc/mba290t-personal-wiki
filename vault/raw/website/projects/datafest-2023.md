---
title: "DataFest 2023 — ASA Data Analysis Competition"
description: "48 hours on the American Bar Association's free legal advice platform — and the finding that the categories with the fewest cases were the ones going unanswered."
summary: "An open brief, real data, and 48 hours. I led a five-person team and owned the analysis: the categories with the fewest cases carried the highest non-response rates — and our own recommendation system retrieved worst in exactly those categories. Won Best Insight."
role: "Team lead · trend analysis and framing"
period: "2023 · 48 hours"
depth: "project"
org: "University of Notre Dame"
badges: ["Best Insight"]
live: false
tags: ["analytics", "research", "product"]
metrics:
  - n: "48"
    l: "hours, prompt to submission"
  - n: "Best Insight"
    l: "prize, 10–15 teams"
  - n: "5"
    l: "person team, 3 disciplines"
links: {}
featured: false
order: 9
---

**Host:** Notre Dame's statistics department

> **The 30-second version.** The American Statistical Association hands you a dataset, an open brief and **48 hours**. Ours was the American Bar Association's platform, where people on low incomes post legal questions and volunteer lawyers answer them free. The intuitive read is that the busiest areas of law fall furthest behind. The data said the reverse — and that reversal is what the submission was built on, including what it implied about the system we were proposing ourselves.

---

## 1. The brief, and the clock

The ABA platform connects low-income clients with volunteer attorneys for free advice. The brief
asked us to advise the ABA and its state partners on general trends, identify where expertise was
short, and help prepare volunteers for the questions coming at them.

That is an open brief — three directions, no specified question, and no indication of what a good
answer looks like. Forty-eight hours from receiving the prompt and the data to submitting, with
ten to fifteen other teams working the same problem.

## 2. What was mine

Worth stating plainly, because this was a team of five across business analytics, computer science
and mathematics, and the deliverable has two halves.

**Mine:** leading the team — organising the flow of work and who did what — the descriptive trend
analysis, and the framing that turned it into an argument.

**Not mine:** the similarity model and the system architecture. Teammates built the retrieval
approach, pairing category matching with Sentence-BERT embeddings over post content and a weighting
that discounts anything filed under the catch-all "Other" category.

The two halves needed each other, and the section below is about the point where they met.

An open brief and a fixed deadline interact badly: five people will each optimise a different
reading of the problem unless the framing is settled early, and at 48 hours there is no time to
converge late. Getting the question fixed was the first job, before any of the analysis.

## 3. What the data said

The descriptive pass produced the map of where the platform was struggling:

- **Unanswered questions cluster by region and category.** Education carried the largest share of
  unresolved questions across Southern states; income-related questions the largest share across
  Central ones.
- **Juvenile and individual rights** had the highest proportion of non-response nationally.
- **Family and children**, the single largest category by volume, had a *relatively low*
  proportion of non-response.
- **Response times were improving** year over year, decaying roughly exponentially — but with a
  consistent seasonal bulge in Q2.
- **The worst single wait** was work, employment and unemployment questions in South Carolina, at a
  median of 26 days, followed by family and children, then health and disability.

That last one is directly actionable on its own: ranking median response time by category and state
tells the ABA where another volunteer attorney buys the most.

## 4. The finding that inverted the expectation

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 214" role="img" aria-labelledby="df-t" xmlns="http://www.w3.org/2000/svg">
 <title id="df-t">A reinforcing cycle: few cases in a category produce a thin corpus, which produces weaker similarity matches, which produces slower or no response, which keeps the category sparse</title>
 <defs>
  <marker id="df-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
  <rect x="8" y="34" width="150" height="56" rx="8" fill="var(--surface)" stroke="var(--gold)"/>
  <text x="83" y="58" font-size="10" fill="var(--ink)">Few cases in</text>
  <text x="83" y="74" font-size="10" fill="var(--ink)">a category</text>
  <path d="M158 62 L180 62" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#df-ar)"/>
  <rect x="184" y="34" width="150" height="56" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="259" y="58" font-size="10" fill="var(--ink)">Thin corpus to</text>
  <text x="259" y="74" font-size="10" fill="var(--ink)">retrieve from</text>
  <path d="M334 62 L356 62" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#df-ar)"/>
  <rect x="360" y="34" width="150" height="56" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="435" y="58" font-size="10" fill="var(--ink)">Weaker similarity</text>
  <text x="435" y="74" font-size="10" fill="var(--ink)">matches</text>
  <path d="M510 62 L532 62" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#df-ar)"/>
  <rect x="536" y="34" width="156" height="56" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="614" y="58" font-size="10" fill="var(--ink)">Slower or no</text>
  <text x="614" y="74" font-size="10" fill="var(--ink)">response</text>
  <path d="M614 90 L614 132 L83 132 L83 94" stroke="var(--gold)" stroke-width="1.4" fill="none" marker-end="url(#df-ar)"/>
  <text x="350" y="150" font-size="9.5" fill="var(--gold)">the category stays sparse, and the loop tightens</text>
  <text x="350" y="180" font-size="10.5" fill="var(--ink-2)">0.748 top match for a well-populated family law question.</text>
  <text x="350" y="196" font-size="10.5" fill="var(--ink-2)">0.586 for a sparse education one in the same state.</text>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio from the submitted analysis.</figcaption>
</figure>

Read those findings together and the expectation inverts.

The intuitive story is that the busiest categories are the ones falling behind — most demand, most
backlog, longest waits. The data says the opposite. **Family and children carried the most cases
and a comparatively low non-response rate. The categories with fewer cases were the ones going
unanswered.**

Volume is not what causes questions to go unanswered. It is closer to the thing that prevents it.
A category with sustained volume accumulates volunteers who recognise the work, precedent to lean
on, and a routine for handling it. A category that surfaces occasionally has none of that, and each
question arrives as a one-off to somebody with nothing to pattern-match against.

Which reframes the recruitment question the brief asked. "Where should the ABA find more lawyers"
has an obvious answer — the busiest categories — and it is the wrong one. The need is heaviest in
the thin categories, where there is no volume to justify the attention and no accumulated practice
to make the next question easier.

## 5. Turning it on our own system

The same argument applies to the thing we were proposing.

A retrieval system that surfaces similar past cases can only be as good as the corpus it draws
from. In a dense category it has thousands of near-neighbours; in a sparse one it has almost
nothing. **So our own recommendation system would work worst exactly where the platform was already
failing worst** — same root cause, two symptoms.

We showed it rather than describing it. The submission carried two worked retrievals:

- A **family law** question about custody and health insurance. Top three matches at **0.748,
  0.721, 0.682** — all squarely on-topic, all genuinely usable as a reference.
- An **education** question from South Carolina about a rescinded university offer. Top three at
  **0.586, 0.576, 0.572** — all loosely about college disputes, none about the actual question.

The second example is there on purpose. South Carolina has very few answered education posts, so
there was nothing close to retrieve, and the scores say so.

## 6. Why the failing example was the point

A recommendation demo that shows only its good matches has proved nothing. Every retrieval system
looks excellent on a well-covered query. What a reviewer needs to know is where it stops working
and whether the people proposing it know.

Including the weak case did three things at once. It made the strong case credible, by
demonstrating the scores separate cases that genuinely differ. It gave the ABA an operational rule
— **trust the recommendation above a threshold, route below it to a human** — which is more useful
than a system presented as uniformly reliable. And it tied the system back to the trend finding,
so the two halves of the submission argued for each other instead of sitting side by side.

The prize was for **insight**, not for the model. That distinction matters to how this page should
be read: the modelling was my teammates' work, and what I contributed was the finding, and the
decision to point it at our own proposal rather than away from it.
