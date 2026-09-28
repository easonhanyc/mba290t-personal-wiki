---
title: "Kickstarter Scraper"
description: "The tool the course taught returns an empty result on this page — and not an error. Working out why is the whole project."
summary: "rvest cannot scrape this page on its own, and it fails silently: Kickstarter builds its campaign body in the browser, so parsing the server's reply finds nothing and reports nothing. The fix is a two-stage pipeline — drive a real browser, snapshot the document it builds, then parse the snapshot."
role: "Individual extra credit · ITAO 40450, Mendoza College of Business"
period: "Spring 2023"
depth: "project"
org: "University of Notre Dame"
badges: ["Browser automation"]
live: false
tags: ["eng", "research"]
metrics:
  - n: "2"
    l: "runtimes, one pipeline"
  - n: "6"
    l: "fields extracted per project"
  - n: "0"
    l: "requests per parse retry"
  - n: "Empty"
    l: "what the naive approach returns"
links: {}
featured: false
order: 11
---
> **The 30-second version.** Pull a Kickstarter project's headline numbers off the page. On most sites that is fifteen lines of `rvest` and an afternoon. On Kickstarter the most valuable field comes back **empty** — and not with an error. The project is really about why that happens, and what you do instead: let a real browser execute the page, capture the document it builds, and parse that.

---

## 1. Why the obvious approach finds nothing

`rvest` fetches the HTML a server sends and parses it as a document. That is the right model for
most of the web, and it was the right model for the Formula 1 results archive I scraped three days
later — those pages arrive complete.

Kickstarter's don't. The campaign body — the part carrying the actual pitch — sits under
`#react-campaign`. The selector names the framework, which is the tell. That subtree is not in the
server's response at all; it is assembled by JavaScript in the visitor's browser after the page
loads. Request the URL, parse the reply, and you are reading a document where that section has not
been written yet.

Here is what makes it a trap rather than an inconvenience. `html_elements()` on a selector matching
nothing **does not raise**. It returns a zero-length node set. `html_text()` on a zero-length node
set returns `character(0)`. The script runs to completion, exits cleanly, and prints nothing.

**A scraper that found nothing and a page that contains nothing produce identical output.** There is
no error to read and no stack trace to search — and the selector, which was correct the whole time,
is the first thing you suspect.

## 2. Treating the page as a program, not a document

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 226" role="img" aria-labelledby="ks-t" xmlns="http://www.w3.org/2000/svg">
<title id="ks-t">Two paths: rvest alone requests the URL and finds the react-campaign section absent, returning an empty result; Selenium loads the page in a browser, saves the built DOM to a local file, and rvest parses that snapshot with the same selectors</title>
<defs>
<marker id="ks-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/></marker>
</defs>
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" text-anchor="middle">
<text x="12" y="20" font-size="9.5" fill="var(--ink-3)" text-anchor="start">rvest on its own</text>
<rect x="12" y="28" width="150" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="87" y="54" font-size="10" fill="var(--ink-3)">GET the URL</text>
<path d="M162 50 L182 50" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="186" y="28" width="150" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="261" y="54" font-size="10" fill="var(--ink-3)">Server's HTML</text>
<path d="M336 50 L356 50" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="360" y="28" width="170" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="445" y="46" font-size="10" fill="var(--ink-3)">#react-campaign</text>
<text x="445" y="61" font-size="10" fill="var(--ink-3)">isn't in it</text>
<path d="M530 50 L550 50" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="554" y="28" width="134" height="44" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="621" y="54" font-size="10" fill="var(--ink-3)">character(0)</text>
<text x="12" y="118" font-size="9.5" fill="var(--gold)" text-anchor="start">Selenium, then rvest</text>
<rect x="12" y="126" width="150" height="52" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="87" y="146" font-size="10" fill="var(--ink)">Browser loads</text>
<text x="87" y="162" font-size="10" fill="var(--ink)">and runs the JS</text>
<path d="M162 152 L182 152" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="186" y="126" width="150" height="52" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="261" y="146" font-size="10" fill="var(--ink)">Full DOM, with</text>
<text x="261" y="162" font-size="10" fill="var(--ink)">the campaign</text>
<path d="M336 152 L356 152" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="360" y="126" width="170" height="52" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
<text x="445" y="146" font-size="10" fill="var(--ink)">innerHTML saved</text>
<text x="445" y="162" font-size="10" fill="var(--ink)">to a local file</text>
<path d="M530 152 L550 152" stroke="var(--border-strong)" stroke-width="1.4" marker-end="url(#ks-ar)"/>
<rect x="554" y="126" width="134" height="52" rx="8" fill="var(--surface)" stroke="var(--gold)"/>
<text x="621" y="146" font-size="10" fill="var(--ink)">rvest parses</text>
<text x="621" y="162" font-size="10" fill="var(--ink)">the snapshot</text>
<text x="350" y="206" font-size="10.5" fill="var(--gold)">Same selectors. Different document.</text>
</g>
</svg>
</div>
<figcaption>Redrawn for this portfolio.</figcaption>
</figure>

If the content is built by code, you have to run the code.

**Stage one is a real browser.** Selenium drives Safari's WebDriver to the project URL, lets the page
finish assembling itself, then reads `innerHTML` off `<body>` and writes it to a local file. Safari's
driver is the pragmatic choice on macOS — it ships with the browser, so there is no separate binary
to install and keep in step with a version.

**Stage two is the `rvest` script that was always going to work**, pointed at the file on disk instead
of at the URL. Title, pledged amount, pledge goal, backers, location, description. Six selectors,
unchanged. A different document underneath them.

## 3. Splitting fetch from parse pays twice

Those selectors are long descendant chains, the kind a browser's *copy selector* hands you. Getting
six of them right is iterative: run it, look at what came back, adjust, run it again.

If fetching and parsing were one step, every iteration would be another request to Kickstarter —
dozens of hits on somebody else's servers to debug your own code. With the document already on disk,
iteration costs **nothing** and the site sees a single visit. Practical and polite turn out to be the
same decision.

The [Formula 1 scrape](/work/formula-1-trends) solved that same concern differently, because it had a
different shape: 96 pages across 32 seasons cannot be snapshotted once, so it used `polite::bow()` to
read `robots.txt` and rate-limit itself. One page, save it. Ninety-six, throttle them. The obligation
is constant; the mechanism follows the job.

## 4. Two ways to read text, and the difference shows

`rvest` offers `html_text()` and `html_text2()`. The first returns the raw text nodes, layout
whitespace and all. The second approximates what the browser actually renders — collapsing runs of
whitespace, honouring line breaks.

For the title and the two currency figures — single tokens sitting alone in an element — either works.
For backers, location and the multi-paragraph description, it is the difference between usable text and
text still carrying the shape of the markup around it. Those three use `html_text2()`, and the
description needed one further pass to strip the newlines that survived.

A small detail, and the kind that decides whether the output needs cleaning downstream or not.

## 5. The part worth carrying

What transfers here is not a library. It is a question to ask before writing a single selector: **does
the content I want exist in the response, or is it assembled in the browser?**

View-source and inspect-element disagree exactly when the answer is *assembled* — view-source shows
what the server sent, the inspector shows what the browser built. Comparing the two takes seconds, and
it decides which of two quite different tools the job needs.

Skip that check and the failure is silent, the selector looks wrong when it isn't, and the afternoon
goes to debugging the one part of the pipeline that was already correct.
