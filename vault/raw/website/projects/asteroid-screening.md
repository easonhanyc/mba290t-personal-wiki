---
title: "Hazardous Asteroid Screening"
description: "NASA's definition of a hazardous asteroid is made of two variables — and both were columns in the training data. The first real decision was throwing one away."
summary: "Space agencies cannot watch every near-Earth asteroid closely, so the useful model is a triage filter, not an oracle. That reframing decides which columns you are allowed to use and which error you would rather make — and it rules out the single most predictive variable in the dataset."
role: "Framing, dataset selection, literature and the written argument · ITAO 40420"
period: "Spring 2022"
depth: "project"
org: "University of Notre Dame"
badges: ["Applied ML"]
live: false
tags: ["analytics", "ai", "research"]
metrics:
  - n: "4,687"
    l: "NASA asteroid records"
  - n: "40 → 17"
    l: "variables kept as predictors"
  - n: "92.5%"
    l: "sensitivity, up from 77.1%"
  - n: "0.14"
    l: "decision cut-off, down from 0.50"
links: {}
featured: false
order: 12
---

**Scope:** a two-person research project — the line above is my half of it.

> **The 30-second version.** NASA tracks tens of thousands of near-Earth asteroids and cannot watch all of them closely. So the useful question is not *which asteroids are hazardous* — it is *which ones deserve scarce telescope time first*. That reframing decides everything downstream: which columns the model is allowed to use, and which of the two possible mistakes you would rather make. The first real decision was throwing away the most predictive variable in the dataset, because by the time you know it, the answer has already arrived.

---

## 1. The question behind the question

NASA's Center for Near-Earth Object Studies had identified 26,115 near-Earth asteroids and 2,185
potentially dangerous ones; 888 of those measure more than a kilometre across. Observation is the
bottleneck. The longer an object is watched the better the prediction becomes, and telescope and
compute time are finite — so the constraint is not detection, it is allocation.

That makes the model a **triage filter**, not an oracle: cheap enough to run across everything,
good enough to decide what gets watched properly. It is a different product from a classifier that
is merely accurate, and the difference shows up twice below.

## 2. The definition was sitting in the data

NASA's definition of a potentially hazardous asteroid is exact: an **Earth Minimum Orbit
Intersection Distance of 0.05 au or less, and an absolute magnitude of 22.0 or less.**

Both quantities were columns in the dataset.

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 212" role="img" aria-labelledby="as-t" xmlns="http://www.w3.org/2000/svg">
<title id="as-t">NASA's two-part definition of a potentially hazardous asteroid maps directly onto two columns of the training data: minimum orbit intersection distance was removed because it is not known until the approach, and absolute magnitude was kept and became the top-ranked feature</title>
<defs>
<marker id="as-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/></marker>
</defs>
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
<text x="12" y="16" font-size="9.5" fill="var(--ink-3)" text-anchor="start">NASA: "potentially hazardous" means</text>
<text x="688" y="16" font-size="9.5" fill="var(--ink-3)" text-anchor="end">columns in the training data</text>
<rect x="12" y="26" width="270" height="42" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="147" y="52" font-size="10" fill="var(--ink)">Earth MOID ≤ 0.05 au</text>
<text x="348" y="41" font-size="9.8" fill="var(--ink-3)">the same number</text>
<path d="M282 47 L414 47" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#as-ar)"/>
<rect x="418" y="26" width="270" height="42" rx="8" fill="var(--surface)" stroke="var(--gold)"/>
<text x="553" y="52" font-size="10" fill="var(--ink)">Minimum.Orbit.Intersection</text>
<text x="688" y="84" font-size="9.5" fill="var(--gold)" text-anchor="end">removed — not knowable until the approach</text>
<rect x="12" y="100" width="270" height="42" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="147" y="126" font-size="10" fill="var(--ink)">Absolute magnitude ≤ 22.0</text>
<text x="348" y="115" font-size="9.8" fill="var(--ink-3)">the same number</text>
<path d="M282 121 L414 121" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#as-ar)"/>
<rect x="418" y="100" width="270" height="42" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="553" y="126" font-size="10" fill="var(--ink)">Absolute.Magnitude</text>
<text x="688" y="158" font-size="9.5" fill="var(--ink-2)" text-anchor="end">kept — came back as the top-ranked feature</text>
<text x="350" y="192" font-size="10.5" fill="var(--gold)">Half the label was still in the features.</text>
</g>
</svg>
</div>
<figcaption>Redrawn for this portfolio.</figcaption>
</figure>

Minimum Orbit Intersection Distance is not something you observe early. It is the distance between
the closest points of the two orbits, characterised when the close approach is worked out. A model
fed that column scores beautifully and is operationally worthless, because by the time the value
exists you already have the answer you wanted the model to give you in advance.

So it came out. Not on a statistical test — no correlation screen flags a variable for being *half
of the label* — but on an operational question: **is this knowable at the moment the prediction has
to be made?** For a triage filter the answer has to be yes, or the filter never runs.

## 3. What else came out, and why

The raw data was 4,687 asteroid records across 40 variables. Seventeen survived as predictors.

- **Unit duplicates.** Relative velocity appeared in km/s, km/h and mph; estimated diameter in
  kilometres, metres, miles and feet; miss distance in four units again. Identical information at
  correlation 1.0 — one copy of each kept.
- **Constants.** Every asteroid in the set orbits Earth, and every observation uses the J2000
  equinox. A column with a single value carries no signal, and will keep carrying none as new
  records arrive.
- **Identifiers.** Name and reference ID. Orbit ID went too — categorical, and derivable from the
  orbital characteristics already in the data.
- **Observation dates.** This is not a time series. When somebody happened to look is a fact about
  the observer, not about the asteroid.

Most of that is routine hygiene, and a correlation matrix finds it. Only the MOID decision required
knowing what the model was *for*.

## 4. Accuracy was the wrong headline

Four models, evaluated on a 30% holdout:

| Model | Accuracy | Sensitivity | AUC |
|---|---|---|---|
| Logistic regression | 82.44% | 66.36% | 0.871 |
| Random forest, bagged | 91.83% | 92.52% | 0.979 |
| XGBoost | **94.53%** | 77.10% | 0.980 |
| XGBoost, tuned | 92.54% | **92.52%** | **0.982** |

**The most accurate model is not the one that was chosen.**

Untuned XGBoost classifies more asteroids correctly than anything else in the table and misses
nearly a quarter of the hazardous ones. Tuning gave up two points of accuracy and bought fifteen
points of sensitivity — which is the trade this problem asks for, because the two errors are not
comparable. A false positive spends telescope time on a rock that turns out to be fine. A false
negative is a hazardous asteroid that nobody is watching.

Most of that movement isn't in the model at all. It is in the decision cut-off, dragged from the
default 0.5 down to **0.14** — a threshold that says, in effect, *flag it if there is better than a
one-in-seven chance*. Picking that number is not a modelling decision. It is a judgement about which
mistake you are willing to make more often, and it belongs to whoever owns the consequences rather
than to whoever fits the model.

## 5. The leak that stayed in

The feature importances came back with **absolute magnitude** ranked top.

Absolute magnitude is the other half of NASA's definition.

One component of the label was removed and the other was left in, and the model found it — exactly
as it should have. The write-up flags this in its own limitations rather than presenting the ranking
as a discovery, which is the right call: a variable that appears in the definition of the target is
not evidence about what makes an asteroid dangerous. It is the definition looking back at you.

Read strictly, that limits what the study's second research question — *which characteristics matter
most* — can actually claim. The finding underneath it is the more useful one: perihelion distance,
inclination and perihelion argument are the features carrying information the label does not already
contain.

## 6. Stated limitations

From the report's own future-work section rather than added afterwards:

- **The cut-off was found by hand, not optimised.** Accuracy fell as the threshold moved to chase
  sensitivity, and no sweep was run to locate the best combination of the two. There is a better
  number than 0.14.
- **Absolute magnitude is part of the definition**, so the factors worth studying next are the
  others — perihelion distance, inclination, perihelion argument — and how they relate to hazard.
- **Near-Earth asteroids only.** Meteoroids, comets and other objects are out of scope, and nothing
  here extends to them without new data.
- **Sample size is the binding constraint**, not method. Fewer than five thousand records against
  more than twenty-six thousand known near-Earth objects is not enough to call the model
  generalisable.
