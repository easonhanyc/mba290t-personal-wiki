---
title: "TripMatch"
description: "Sole PM, designer and engineer \u2014 problem framing, PRD, flow design, front end and API, through to production."
summary: "A 400-person class coordinates rides by scrolling a WhatsApp chat, where requests get buried and matching seats go unused. I shipped a verified, Berkeley-only rides board \u2014 and then tested it against its own launch load, which is where the interesting part starts."
role: "Sole PM, designer, and engineer"
period: "Aug 2026"
depth: "case-study"
org: "Independent"
badges: ["0 \u2192 1"]
live: true
tags: ["product", "eng", "shipped"]
metrics: 
  - n: "One board"
    l: "every ride in one place"
  - n: "+1"
    l: "one tap and the seat is yours"
  - n: "No app"
    l: "opens from the group chat"
  - n: "Verified"
    l: "Berkeley classmates only"
links: 
  live: "https://tripmatch-app.github.io/"
  code: "https://github.com/tripmatch-app/tripmatch-app.github.io"
  prd: "/artifacts/tripmatch-prd"
featured: true
order: 1
---

**Timeline:** August 22–27, 2026

> **The 30-second version.** Six days from PRD to a public, verified rides board for the Haas class — problem framing, flow design, front end, API, and two feedback-driven iteration cycles, done alone. The part worth reading is the launch-hardening round, which caught three defects that would have broken the product inside its own expected load, before a single real user hit them. The nastiest of them was caused by the distribution channel the product depends on.

| | |
|---|---|
| **Problem** | Ride coordination lives in an unstructured group chat; matches are found by luck, not by search |
| **Constraint** | No budget, no eng team, no institutional access to CalNet SSO, one week |
| **What shipped** | Verified sign-in, structured board, seat claims with capacity enforcement, comments, audit log, feedback inbox |
| **Evidence of rigor** | 34 commits · 168 automated checks · 3 shipped iterations from real user feedback · a documented pre-launch architecture rebuild |

---

## 1. The problem, and why it wasn't already solved

Haas students regularly need ad-hoc rides — day trips into SF, weekend runs to the South Bay, Sunday returns to campus. All of it is coordinated by word of mouth and by scrolling the class WhatsApp chat.

Three costs fall out of that:

1. **Requests get buried.** A "does anyone have a car Friday?" message is 40 messages deep by evening.
2. **There is no way to see overlap.** Two people driving the same route on the same day never learn about each other.
3. **The failure mode is silent waste.** Empty seats leave on trips that already have room, while classmates pay for solo rideshares.

**The interesting question is not "why hasn't anyone built a carpool app" — plenty have.** Waze Carpool and a string of campus carpool startups mostly failed or stayed niche. My read on why: they all had to manufacture *trust* and *liquidity* between strangers simultaneously, which is the hardest possible cold-start.

A single MBA class already has both. Trust is pre-existing — these are classmates. Liquidity is naturally clustered, because travel demand spikes around shared events: treks, class trips, weekend commutes. **The gap wasn't "no carpool tool exists." It was that nobody had built the version scoped to a small, trusted, high-overlap community rather than a stranger marketplace.**

That reframe is what made a one-week build viable. I wasn't solving matching at scale; I was replacing a group chat's search function for ~400 people who already know each other.

---

## 2. What I deliberately chose *not* to build

Scope discipline was the main reason this shipped in a week. The [PRD's non-goals](/artifacts/tripmatch-prd) were written before any code:

| Non-goal | Reasoning |
|---|---|
| **Not a payments / cost-splitting tool** | Venmo already works. Adding money introduces trust and liability complexity that buys no additional matches. |
| **Not real-time dispatch (not Uber)** | The job is *surfacing the match*. Logistics coordination between two classmates is already a solved problem — they text each other. |
| **Not a WhatsApp replacement** | Final coordination stays in chat. Trying to own the whole conversation would have meant competing with an app that had 100% adoption. |
| **No public/open matching** | Opening to strangers re-introduces the exact trust problem the design exists to avoid. |
| **No native mobile app** | A link is the right form factor — zero install friction, one tap from the group chat where the users already are. |

The last one mattered most. **Distribution determined the form factor.** The product had to open from a tapped WhatsApp link, which later turned out to be the source of the single nastiest bug in the project (§5).

---

## 3. From prototype to launch: what real users changed

V1 went to a slice of the class. Three gaps surfaced within days — all of them things no amount of pre-launch reasoning had surfaced, and all of them shipped in the next round:

**1. No way to remove a post.** A rider whose plans fell through had no way to take a stale post down; it sat on the board until it aged out. *Shipped: owner-scoped Delete with a two-step confirm.*

**2. No way to correct a post.** Changing a pickup time meant deleting and re-posting — which destroyed the comment thread already on the post. *Shipped: an Edit control scoped to the same owner check, which updates in place and preserves comments and original post time.*

**3. The board didn't scale with volume.** Grouping by route + date and listing everything top-to-bottom is fine for a handful of posts. Once the board spanned several trip dates, finding "just Friday's trips" meant scrolling past everything else. *Shipped: a row of date chips with per-date post counts.*

Two product decisions inside that third fix are the ones I'd point to in an interview:

- **The date-chip row only appears once the board spans more than one date.** With a single date it would be redundant with "All dates" — a control that does nothing is worse than no control.
- **It composes with the existing role filter rather than replacing it.** Filters that reset each other are a well-known way to make users feel like the UI is fighting them.

All three were validated against an isolated mock backend — multiple test personas posting, editing, filtering, deleting — so the shared production board was never touched during testing.

---

## 4. The launch-hardening call: killing my own v1 architecture

This is the decision I'm proudest of, because the easy path was to ship.

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 216" role="img" aria-labelledby="tm-t" xmlns="http://www.w3.org/2000/svg">
<title id="tm-t">A link tapped inside WhatsApp opens in that app&#8217;s embedded browser, where a popup sign-in has no opener window to return a credential to, so authentication dies on a blank page</title>
<defs><marker id="tm-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/></marker></defs>
<g font-family="var(--mono)" font-size="10" text-anchor="middle">
<text x="8" y="14" fill="var(--ink-3)" text-anchor="start" letter-spacing="1.2">THE CHANNEL THE PRODUCT DEPENDS ON</text>
<rect x="8" y="26" width="152" height="46" rx="4" fill="var(--surface)" stroke="var(--border-strong)"/><text x="84" y="46" fill="var(--ink)">LINK SHARED IN</text><text x="84" y="62" fill="var(--ink)">THE GROUP CHAT</text>
<path d="M162 49 L196 49" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#tm-a)"/>
<rect x="200" y="26" width="152" height="46" rx="4" fill="var(--surface)" stroke="var(--border-strong)"/><text x="276" y="46" fill="var(--ink)">OPENS IN THE APP&#8217;S</text><text x="276" y="62" fill="var(--ink)">EMBEDDED BROWSER</text>
<path d="M354 49 L388 49" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#tm-a)"/>
<rect x="392" y="26" width="152" height="46" rx="4" fill="var(--surface)" stroke="var(--border-strong)"/><text x="468" y="46" fill="var(--ink)">POPUP SIGN-IN</text><text x="468" y="62" fill="var(--ink)">HAS NO OPENER</text>
<path d="M546 49 L580 49" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#tm-a)"/>
<rect x="584" y="26" width="108" height="46" rx="4" fill="var(--surface)" stroke="var(--gold)" stroke-width="1.6"/><text x="638" y="53" fill="var(--gold)">BLANK PAGE</text>
<text x="350" y="116" fill="var(--ink-2)" font-size="11">The distribution channel and the single point of auth failure were the same thing.</text>
<text x="350" y="140" fill="var(--ink-3)">INVISIBLE IN DESKTOP TESTING &#183; FOUND IN THE LAUNCH-HARDENING ROUND</text>
<line x1="140" y1="164" x2="560" y2="164" stroke="var(--border-strong)"/>
<text x="350" y="192" fill="var(--ink-3)">3 DEFECTS FOUND IN MY OWN V1 &#183; 168 AUTOMATED CHECKS &#183; 6 DAYS TO LAUNCH</text>
</g>
</svg>
</div>
<figcaption>Redrawn for this portfolio.</figcaption>
</figure>

Prototype feedback produced the three product gaps above. Preparing for *public* launch surfaced a different class of problem entirely: **the v1 storage design would not have survived the class it was built for.** V1 stored the whole board as one JSON document in a hosted-JSON service. Against the expected load — ~400 students, ~200 concurrent posts — it had three defects:

| Defect | Consequence if launched |
|---|---|
| API key published in page source | **Any visitor could wipe the entire board.** The key was account-wide, not scoped to one document, and visible in View Source. |
| Whole-board read-modify-write | **Simultaneous posts silently overwrote each other.** Two people acting inside one HTTP round trip (~200–600ms on mobile) meant one post vanished — with no error shown. |
| One 100 KB document cap | **The board freezes at roughly 100–150 posts** with comments — about half the expected peak. |

The second one is the one worth dwelling on, because it's a product failure disguised as a technical one. The user experience of that race condition is: *you post, you see your post appear, and on your next refresh it's silently gone.* The natural user response is to post again — which is exactly the burst behavior that makes the race more likely. **Launch day means a WhatsApp link landing in front of 400 people at once, which is precisely the load that triggers it.**

I rebuilt the storage layer behind an API before launch instead of after:

```
GitHub Pages (static) → Cloudflare Worker → D1 (SQLite)
         ↕
Google Identity Services (berkeley.edu domain only)
```

**The rule that shaped the design: the browser holds no secret and performs no write.** It holds a session token proving who the user is; the server decides what that person may do.

Three things fell out of that, each of which resolved an open question the PRD had been carrying:

- **Verified identity.** True CalNet SSO requires UC Berkeley IT to register the app as an approved Service Provider — an application and a review process a student project can't clear. But Berkeley's bMail runs on Google Workspace, so *every CalNet holder already has a Google account on the `berkeley.edu` domain*. Google Sign-In restricted to that domain, verified server-side against Google's published keys, delivers verified identity with zero IT involvement. A personal Gmail is rejected at the door.
- **Ownership became real.** Edit/Delete had compared a name typed into a box against a name in browser storage. That meant you lost control of your post when you switched from laptop to phone, *and* anyone could type your name to seize it. Ownership is now an email match against a verified account, enforced server-side.
- **Honest failure states.** V1's worst bug: when the backend was unreachable, the page rendered **"Nothing posted yet"** — which reads as an empty board and invites a duplicate post. A total outage looked identical to a quiet day. There is now one banner covering offline / unreachable / server error / rate limited / expired session, each naming the action that might fix it.

**Verification:** 168 automated checks against the real worker and real SQL — including a concurrency test that fires 36 simultaneous writes and asserts all survive (the v1 design fails this), and one that fires ten simultaneous claims at a one-seat car and asserts exactly one wins.

---

## 5. Two product judgment calls worth reading

**Seat claims are role-dependent, and that's the whole point.**

"+1" was ambiguous on a driver's post — it read as either *"I want a seat"* or *"I'm also driving that way."* And nothing enforced capacity, so six people could +1 a three-seat car. The fix wasn't to add a cap everywhere; it was to notice that **the same interaction means different things on the two sides of the marketplace**:

- On a **driver's** post: a capped **seat claim**, with a counting-down badge and a `Full` state. Over-claiming is a real-world failure — a driver arriving to find more people than seats.
- On a **rider's** post: an uncapped **+1**. Several riders wanting the same trip isn't a conflict; it's *demand signal to a driver*. Capping it would destroy the most useful information on the board.

The cap is enforced inside the `INSERT`, not in the UI, so two people tapping the last seat at the same instant cannot both get in.

Party size followed the same logic: a claim can cover a traveller plus family or friends without a Berkeley email, so remaining seats is the *sum of party sizes*, not a count of claims — a driver can tell three claims from four passengers. **Driver posts have no party field**, because their seat count already states the places free for other people.

**The in-app-browser bug — where distribution and authentication collide.**

A link tapped in WhatsApp opens in that app's built-in browser. Google's popup sign-in has no window to return a credential to there, so it dies on a blank page. **The product's entire distribution channel was also its single point of auth failure**, and it was invisible in desktop testing.

The fix ships in two layers: detect those browsers and switch to Google's redirect flow, which needs no popup — and for the ones Google refuses outright, give the user an explicit way out to Safari or Chrome rather than a dead end.

---

## 6. How success is measured

Defined in the PRD before launch, deliberately split so leading indicators could steer while lagging indicators were still accumulating:

**Leading** — trip posts per week · % of posts receiving a matching counterpart within 48h · median time from post to match · % of new users who verify *and* post or browse in their first session

**Lagging** — repeat usage rate (does a first-time poster come back for their next trip) · qualitative preference signal vs. the WhatsApp chat

Target from the PRD: **a user can post or find a match in under two minutes.**

The honest caveat I'd give in an interview: there is **no pre-existing baseline**, because the incumbent behavior is informal chat with nothing instrumented. "Faster than scrolling WhatsApp" can be demonstrated, but not cleanly A/B'd. That's a real limitation of the measurement design, not something to paper over.

---

## 7. What I'd do differently

- **I should have designed the storage layer for the launch load, not the prototype load.** The rebuild cost a full day under time pressure. Choosing the JSON-blob store was the right call for a two-day prototype and the wrong one to carry toward a 400-person launch — and I didn't re-examine it until launch prep forced me to.
- **The in-app browser failure should have been caught in the PRD, not in production.** I wrote "distribution is a WhatsApp link" as a *goal* and never traced it through to "therefore auth must work inside WhatsApp's browser." The insight is that distribution channel choices are technical constraints, not just growth decisions.
- **Post-expiry needs a notification decision.** An expired post disappears silently; anyone who'd claimed a seat gets no signal. Still an open question in the PRD — logged rather than quietly dropped.
- **The domain gate proves `berkeley.edu`, not Haas.** Since the link circulates in the Haas chat this is probably fine, but an allow-list could tighten it. My recommendation was to *watch the activity log for unexpected sign-ins before acting* rather than pre-emptively narrowing access — cheaper to observe than to over-engineer.

---

## Artifacts

| Artifact | What it shows |
|---|---|
| [Product Requirements Document](/artifacts/tripmatch-prd) | Problem framing, non-goals, user stories, P0/P1/P2 requirements with acceptance criteria, success metrics, open questions |
| [Infrastructure & scalability analysis](/artifacts/tripmatch-infrastructure) | The pre-launch architecture review — what would have broken, at what load, and the mitigation |
| <a href="https://tripmatch-app.github.io/" target="_blank" rel="noopener noreferrer" aria-label="Live product (opens in a new tab)">Live product</a> | The shipped app |
| <a href="https://github.com/tripmatch-app/tripmatch-app.github.io" target="_blank" rel="noopener noreferrer" aria-label="Source repository (opens in a new tab)">Source repository</a> | 34 commits, 168 automated checks, deploy runbook |

---
