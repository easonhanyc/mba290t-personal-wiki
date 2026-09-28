---
title: "Formula 1 Racing Trends"
description: "Thirty-two seasons scraped from Formula 1's own results pages — and the discovery that the hard part was never the model, it was making any two numbers comparable."
summary: "The variable I needed — car speed — is not published by Formula 1. Deriving it forced three separate decisions about comparability, each one paid for in sample size. The modelling took a paragraph; the preprocessing took the project."
role: "Individual project · ITAO 40450, Mendoza College of Business"
period: "Spring 2023"
depth: "project"
org: "University of Notre Dame"
badges: ["Time series & clustering"]
live: false
tags: ["analytics", "research"]
metrics:
  - n: "32"
    l: "seasons scraped, 1991–2022"
  - n: "3"
    l: "datasets built from scratch"
  - n: "1"
    l: "Grand Prix kept, to make seasons comparable"
  - n: "6"
    l: "trend models compared by RMSE"
links: {}
featured: false
order: 10
---

**Scope:** scraping, cleaning, modelling and the write-up — start to finish

> **The 30-second version.** I wanted to know whether Formula 1 cars have actually got faster over three decades, and which teams and drivers the record really favours. Formula 1 publishes results, not speed — so the headline variable had to be constructed. Constructing it exposed **three separate places where the raw numbers were not comparable to each other**, and every fix cost sample size. The analysis that came out the other side is only worth reading because of what happened before it.

---

## 1. The variable that wasn't in the data

Formula 1's results pages publish, for every race, the winner, the number of laps and the winner's
completion time. They do not publish speed.

So speed had to be derived: **race distance ÷ the winner's completion time**, with every time value
converted to minutes for consistency. That produces a clean number — the winner's average speed
over the race, in km/min — from two columns that were already there.

It also produces a problem, because now the metric depends on race distance, and race distance is
not a constant.

I built the inputs by scraping the official results archive with `rvest`, one CSS selector per
table and a loop over every season from 1991 to 2022, into three datasets: **races** (winner, laps,
completion time per Grand Prix), **drivers** (annual standing, nationality, season points) and
**teams** (annual standing, season points). 1991 is the start because the points system introduced
that year is broadly the one still in use.

The scrape was not clean. Two race times came back in a format inconsistent with the rest and had
to be repaired before any time arithmetic would parse; a missing driver standing and a missing team
standing were filled by checking the source pages by hand. Unglamorous, and the whole analysis
depends on it — a silently malformed time value doesn't error, it just produces a fast lap.

## 2. Three ways the numbers weren't comparable

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 252" role="img" aria-labelledby="f1-t" xmlns="http://www.w3.org/2000/svg">
<title id="f1-t">A funnel: every race from 1991 to 2022 narrows to 32 Spanish Grands Prix once speed is derived and the circuit is held constant</title>
<defs>
<marker id="f1-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/></marker>
</defs>
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
<rect x="20" y="8" width="660" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="350" y="36" font-size="10.5" fill="var(--ink)">Every race, every driver, every team · 1991–2022</text>
<path d="M350 52 L350 64" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#f1-ar)"/>
<rect x="90" y="68" width="520" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="350" y="96" font-size="10.5" fill="var(--ink)">Speed isn't published — derive it from distance ÷ time</text>
<path d="M350 112 L350 124" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#f1-ar)"/>
<rect x="160" y="128" width="380" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="350" y="156" font-size="10.5" fill="var(--ink)">Circuits differ — hold the track constant</text>
<path d="M350 172 L350 184" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#f1-ar)"/>
<rect x="210" y="188" width="280" height="52" rx="8" fill="var(--surface)" stroke="var(--gold)"/>
<text x="350" y="210" font-size="10.5" fill="var(--ink)">32 Spanish Grands Prix</text>
<text x="350" y="228" font-size="10" fill="var(--gold)">one comparable point per season</text>
</g>
</svg>
</div>
<figcaption>The chain of constraints behind a single derived metric. Redrawn for this portfolio.</figcaption>
</figure>

**Circuits differ, so a pooled average measures the track.** Averaging derived speed across every
race in a season doesn't describe the cars — it describes which circuits happened to be on that
year's calendar. The only way to compare 1991 to 2022 is to hold the track constant, so I checked
which Grand Prix had the most complete run across the window and the most stable circuit length.
Spain won on both counts, and the speed analysis uses Spain alone.

That is the expensive decision on this page. Roughly seventeen races a season become one. Thirty-two
data points is a thin time series, and I chose it deliberately: **a small valid comparison beats a
large invalid one**, and pooling across circuits would have produced a smooth, confident, meaningless
trend line.

**Even one circuit changes.** Barcelona ran at 4.728 km per lap through 2003 and 4.655 km from 2004,
so distance is computed against the lap length in force that year rather than a single constant.

**The points system changed in 2010**, raising the points available in every race. Raw season points
therefore aren't comparable across that break, and any ranking built on them would simply rediscover
the rule change. I normalised points within each era separately and combined them by their mean.
Drivers and teams with fewer than five seasons were dropped — a single-season average is noise, not
a career.

## 3. What the speed curve actually shows

Plotted as a time series, the winner's average speed at Spain rises steadily to around 2005, falls
sharply, and recovers partially in the mid-2010s. Two values before 2000 sit well off the trend.

The shape is not a technology curve. It tracks **regulation**: the era ending around 2005 paired
some of the most powerful engines ever raced with a low minimum car weight, the rules then changed,
and the turbo-hybrid generation clawed speed back later. Read without that context, the mid-2000s
decline looks like Formula 1 getting worse at building cars.

This is also the honest limit of the method, and it was worth writing down at the time: a fitted
trend line catches the general direction and smooths away exactly the discontinuities that explain
it. The curve tells you *that* something changed in 2005. Only the rulebook tells you what.

## 4. The model that won, and why that is worth doubting

I fitted six candidates to the series — linear, quadratic, cubic, quartic, quartic with an
exponential transform, and Holt-Winters exponential smoothing — and compared them on root mean
squared error. The quartic exponential model came out lowest.

It is also the result I trust least, for a reason visible in the method rather than the output: the
exponential transform changes the scale on which residuals are measured, so part of that model's
advantage is mechanical rather than a better description of the data. Selecting on RMSE across a
transformed and an untransformed model is not a like-for-like comparison — which is the same
comparability problem as section 2, arriving one more time, now inside the model selection itself.

So the result travels with its caveat attached rather than leaving someone else to find it.
A model that wins on a metric it partly redefines is still the winner — but nobody should have
to ask a follow-up question to learn that.

## 5. Clustering, and what unsupervised output is worth

For teams and drivers I used k-means over two features — average annual standing and normalised
points — with a fixed seed and 25 random starts, so the result is reproducible rather than a
function of where the centroids happened to land.

It returned **Mercedes** as the strongest team of the period, with Ferrari and Red Bull in the same
top tier, and **Lewis Hamilton** as the strongest driver, alongside Schumacher, Alonso and
Verstappen.

Any Formula 1 fan could have told me that. **That is what it was for.**

An unsupervised model has no answer key. There is no held-out set, no accuracy to report, and
nothing that tells you whether the clusters mean anything or whether you have simply partitioned
your own preprocessing errors. The only available check is external: facts the model never saw.
Mercedes won eight consecutive constructors' titles from 2014 to 2021. Hamilton has seven drivers'
championships and more race wins than anyone in the sport's history. None of that was in the feature
set — the model saw two normalised numbers per season and nothing else.

Getting those names back out is a check on the entire chain behind them, and specifically on the
2010 normalisation, which was the step most likely to fail quietly. Had the clusters crowned a
midfield team, that would not have been a discovery. It would have been a bug, and I would not have
known which line caused it without something outside the data to fail against.

The part that wasn't predictable was the structure. The number of clusters was chosen by silhouette
score rather than by habit, run separately on each dataset — and it came back **three tiers for
teams but only two for drivers**. Team outcomes spread across a middle; driver outcomes separate
more cleanly into two groups than into three.

## 6. What I'd do differently

Two assumptions in this project are weaker than the results built on them.

**Weather is missing entirely.** Race times reflect conditions, and a wet Spanish Grand Prix
produces a slow winner for reasons that have nothing to do with the car. At least some of the
fluctuation the trend line smooths over — and quite possibly both pre-2000 outliers — is rain being
read as engineering. Conditions belong in the model before the trend is taken seriously.

**Averaging the two points eras isn't enough.** Normalising within each era and taking the mean
narrows the gap but does not close it: drivers and teams competing after 2010 still come out ahead
of comparable ones before it. Hamilton and Schumacher both hold seven championships, and the
post-2010 record consistently scores higher. The two periods need proper weighting rather than an
equal average — otherwise the ranking is still partly reporting the 2010 rule change.
