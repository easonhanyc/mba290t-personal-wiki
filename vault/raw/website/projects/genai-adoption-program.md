---
title: "GenAI Adoption Program"
description: "A gamified adoption programme for 1,100 LATAM sellers — built so that participating, not winning, was the thing being rewarded."
summary: "GenAI tooling existed; usage didn't. Mandating it produces compliance, not adoption — so the programme paid out on activity rather than on rank, giving the 99% who will never top a leaderboard a reason to take part. Over 75% of 1,100 sellers did, inside 60 days."
role: "Product owner · with the LATAM sales director and a principal seller"
period: "2024"
depth: "project"
org: "Amazon Web Services"
badges: ["Go-to-market"]
live: false
tags: ["gtm", "product", "ai"]
metrics:
  - n: "1,100"
    l: "LATAM sellers"
  - n: ">75%"
    l: "participation in 60 days"
  - n: "Weekly"
    l: "and monthly ranking cadence"
links: {}
featured: false
order: 6
---
<aside class="note"><strong>Confidentiality note.</strong> Written at the level of detail already public on my resume. The programme's branding, internal materials, participant names, logins, teams and standings are all omitted — the source material is internal and personally identifying. What is described is the mechanic design.</aside>

> **The 30-second version.** A leaderboard rewards the people already at the top — precisely the group that needs no convincing. This programme was built the other way round: activity earns points, points earn raffle entries, and an entry improves your odds whoever you are. Rankings, badges, prizes and live recognition sat on top of that, but the raffle is what turned a competition into a participation number. **Over 75% of 1,100 LATAM sellers** took part within **60 days**.

---

## 1. The tool was never the constraint

The productivity case for sellers using GenAI in their daily work was not in dispute. The tools existed and were available.

They were not being used, which makes this an adoption problem, and adoption problems are not solved by the thing that solves capability problems. There was nothing to build and nothing to fix. The gap was entirely between *available* and *habitual*.

**Mandating it was the obvious move and the wrong one.** You can require a seller to log a GenAI interaction. You cannot require them to find it useful, and the first requirement produces exactly enough activity to satisfy the second. Compliance-shaped usage looks like adoption in the reporting and produces none of the value, which is worse than low usage because it also destroys your ability to measure the problem.

What was needed was voluntary repetition — people choosing to use it again, often enough to discover for themselves whether it helped.

## 2. Why this needed the field, not the analytics team

I partnered with the **LATAM sales director** and a **principal seller** rather than designing it inside the data org.

That is a deliberate choice about legitimacy. A points programme invented by an analytics function and pushed at a sales org reads as surveillance with a scoreboard attached. The same programme carried by a respected senior seller reads as a challenge from a peer. The mechanics can be identical; the reception is not.

The principal seller also supplies something an analytics team structurally cannot: a reliable answer to *"would I personally bother with this."*

## 3. The mechanics, and what each one buys

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 246" role="img" aria-labelledby="ga-t" xmlns="http://www.w3.org/2000/svg">
 <title id="ga-t">GenAI activity earns points, which feed three parallel reward paths — ranking, badges and raffle entries — that in turn drive further activity</title>
 <defs>
  <marker id="ga-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace">
  <rect x="8" y="58" width="132" height="72" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="74" y="86" font-size="10.5" fill="var(--ink)" text-anchor="middle">GenAI activity</text>
  <text x="74" y="104" font-size="9.8" fill="var(--ink-3)" text-anchor="middle">several qualifying</text>
  <text x="74" y="116" font-size="9.8" fill="var(--ink-3)" text-anchor="middle">activity types</text>
  <path d="M140 94 L176 94" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#ga-ar)"/>
  <rect x="180" y="70" width="96" height="48" rx="8" fill="var(--tag-bg)" stroke="var(--accent)"/>
  <text x="228" y="98" font-size="11" fill="var(--ink)" text-anchor="middle">points</text>
  <path d="M276 86 L316 46" stroke="var(--border-strong)" stroke-width="1.3" marker-end="url(#ga-ar)"/>
  <path d="M276 94 L316 94" stroke="var(--border-strong)" stroke-width="1.3" marker-end="url(#ga-ar)"/>
  <path d="M276 102 L316 142" stroke="var(--border-strong)" stroke-width="1.3" marker-end="url(#ga-ar)"/>
  <rect x="320" y="18" width="236" height="52" rx="7" fill="var(--surface)" stroke="var(--border)"/>
  <text x="336" y="40" font-size="10.5" fill="var(--ink)">Weekly + monthly rank</text>
  <text x="336" y="57" font-size="9.8" fill="var(--ink-3)">the month resets; all-time does not</text>
  <rect x="320" y="74" width="236" height="44" rx="7" fill="var(--surface)" stroke="var(--border)"/>
  <text x="336" y="92" font-size="10.5" fill="var(--ink)">Badge beside your name</text>
  <text x="336" y="108" font-size="9.8" fill="var(--ink-3)">status, not compensation</text>
  <rect x="320" y="122" width="236" height="52" rx="7" fill="var(--surface)" stroke="var(--gold)"/>
  <text x="336" y="144" font-size="10.5" fill="var(--ink)">Raffle entries</text>
  <text x="336" y="161" font-size="9.8" fill="var(--gold)">a reason to play without winning</text>
  <path d="M556 96 L596 96" stroke="var(--border-strong)" stroke-width="1.3" marker-end="url(#ga-ar)"/>
  <rect x="600" y="70" width="92" height="52" rx="7" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="646" y="92" font-size="10" fill="var(--ink)" text-anchor="middle">Prizes and</text>
  <text x="646" y="106" font-size="10" fill="var(--ink)" text-anchor="middle">live events</text>
  <path d="M646 122 L646 198 L74 198 L74 132" stroke="var(--accent)" stroke-width="1.3" fill="none" marker-end="url(#ga-ar)"/>
  <text x="360" y="214" font-size="9.5" fill="var(--accent)" text-anchor="middle">recognition is visible to peers, which is what drives the next round</text>
  <text x="350" y="238" font-size="10.5" fill="var(--ink-2)" text-anchor="middle">Three reward paths, because a single ranking only motivates the people near the top of it.</text>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio. Programme branding, activity definitions and point values omitted.</figcaption>
</figure>

**Points per qualifying activity.** Making the behaviour countable is what makes everything downstream possible. It also fixes what "using GenAI" means, which is otherwise an argument.

**Weekly *and* monthly ranking.** Two cadences doing two jobs. Weekly is tight enough that what you do this week shows up while you still remember doing it. Monthly gives the competition a reset — and the reset is the important half. On a single cumulative leaderboard, anyone outside the top few is permanently out of contention by week three, and a contest you cannot win is a contest you stop reading. A month that starts level puts everyone back in the running twelve times a year.

**Badges beside the name.** A prize is consumed. A badge persists on every leaderboard afterwards, which makes it a different kind of reward — status rather than compensation — and status does not have to be re-bought each month.

**Raffle entries earned through activity.** This is the mechanic I would point to, because it is the one that produces a participation number rather than a leaderboard.

Ranking rewards the top. If the only prize goes to first place, the rational response for the other 1,090 people is not to bother — and a programme where 1% competes hard and 99% ignore it has failed even if the top of the board looks impressive. **Activity-weighted raffle entries give everyone a return on participating rather than on winning.** You cannot out-compete the top seller, but you can improve your odds, and that is a reason to take part available to the entire population.

Over 75% participation is the shape that mechanic produces. A pure ranking does not produce it.

**Live recognition events.** Winners announced to peers rather than published to a dashboard. Recognition that nobody witnesses is a database row.

## 4. The leaderboard has to be believed

One detail from running it that I would carry anywhere: standings were published provisionally with **an explicit window to dispute them** before being finalised, with a stated deadline to raise a correction.

That looks like an administrative courtesy and it is a trust mechanism. A leaderboard derived from activity data will contain errors — attribution gaps, mis-mapped records, timing edges. The first time a participant sees their own contribution missing and has no way to challenge it, they stop believing the board, and shortly after that they stop playing.

**Publishing a correction window converts the errors from a credibility problem into a process.** It also improves the data, because 1,100 people checking their own row is a far better audit than any single analyst.

## 5. What changed while it ran

The programme was revised as it went, and the revisions share a pattern — each one widened who could realistically compete:

- **Country-level standings**, alongside the regional board. A LATAM-wide ranking buries someone who is leading their own country, and the local contest is the one their peers can see them in.
- **More qualifying activity types**, so that different roles had a credible path to points rather than the mechanic favouring whichever job function happened to generate the most of one thing.
- **Certifications as an earning path**, weighted by difficulty. This is the change I find most interesting, because it moves the programme from rewarding *usage* to also rewarding *capability*. Activity points measure that someone tried the tool; a certification measures that they can actually use it. Adding the second without removing the first means the programme stops being purely about logging behaviour and starts also building the skill the behaviour depends on.
