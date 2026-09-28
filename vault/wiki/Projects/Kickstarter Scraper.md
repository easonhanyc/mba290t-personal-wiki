---
title: Kickstarter Scraper
type: project
summary: 'Kickstarter Scraper was an individual extra-credit project for ITAO 40450 at Notre Dame''s Mendoza College of Business (Spring 2023). rvest returned an empty result rather than an error, because Kickstarter builds its campaign body in the browser; the fix was a two-stage pipeline: drive a real browser, snapshot the document it builds, then parse the snapshot.'
sources:
- path: raw/website/projects/kickstarter-scraper.md
  source_id: website-projects-kickstarter-scraper-1a197c60
  sha256: 1a197c6079274012265036b82bd3c0a530846f05e8b0f6cd1a5891a7ada01dbc
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-28T15:10:37'
reviewed: true
reviewed_by: Claude (Anthropic), for Eason Han; each fact checked against the cited passage
reviewed_at: 2026-09-28T15:11
---

# Kickstarter Scraper

Kickstarter Scraper was an individual extra-credit project for ITAO 40450 at Notre Dame's Mendoza College of Business (Spring 2023). rvest returned an empty result rather than an error, because Kickstarter builds its campaign body in the browser; the fix was a two-stage pipeline: drive a real browser, snapshot the document it builds, then parse the snapshot.

## Key facts
- On Kickstarter, the tool the course taught (rvest) returned an empty result for the most valuable field, and not an error. ([[raw/website/projects/kickstarter-scraper|website/projects/kickstarter-scraper.md › front matter]])
- rvest cannot scrape this page on its own, and it fails silently: Kickstarter builds its campaign body in the browser, so parsing the server's reply finds nothing and reports nothing. ([[raw/website/projects/kickstarter-scraper|website/projects/kickstarter-scraper.md › front matter]])
- The project is about why that happens and what to do instead: let a real browser execute the page, capture the document it builds, and parse that. ([[raw/website/projects/kickstarter-scraper|website/projects/kickstarter-scraper.md]])
- Unlike pages that arrive complete, Kickstarter's campaign body (the actual pitch) sits under #react-campaign and is assembled by JavaScript in the visitor's browser after the page loads. ([[raw/website/projects/kickstarter-scraper#1. Why the obvious approach finds nothing|website/projects/kickstarter-scraper.md › 1. Why the obvious approach finds nothing]])
- The failure is silent: html_elements() on a selector that matches nothing does not raise, and html_text() on the empty result returns character(0), so the script exits cleanly and prints nothing. ([[raw/website/projects/kickstarter-scraper#1. Why the obvious approach finds nothing|website/projects/kickstarter-scraper.md › 1. Why the obvious approach finds nothing]])
- Stage one: Selenium drives Safari's WebDriver to the project URL, lets the page finish assembling itself, and writes the body's innerHTML to a local file. ([[raw/website/projects/kickstarter-scraper#2. Treating the page as a program, not a document|website/projects/kickstarter-scraper.md › 2. Treating the page as a program, not a document]])
- Stage two: the unchanged rvest script parses the file on disk instead of the URL, with six selectors for title, pledged amount, pledge goal, backers, location and description. ([[raw/website/projects/kickstarter-scraper#2. Treating the page as a program, not a document|website/projects/kickstarter-scraper.md › 2. Treating the page as a program, not a document]])
- Splitting fetch from parse means iterating on the selectors costs nothing and the site sees a single visit. ([[raw/website/projects/kickstarter-scraper#3. Splitting fetch from parse pays twice|website/projects/kickstarter-scraper.md › 3. Splitting fetch from parse pays twice]])
- Backers, location and the description use html_text2(), which approximates the rendered text; html_text() returns raw text nodes, layout whitespace and all. ([[raw/website/projects/kickstarter-scraper#4. Two ways to read text, and the difference shows|website/projects/kickstarter-scraper.md › 4. Two ways to read text, and the difference shows]])
- The transferable lesson is a question to ask before writing any selector: does the content exist in the server's response, or is it assembled in the browser? ([[raw/website/projects/kickstarter-scraper#5. The part worth carrying|website/projects/kickstarter-scraper.md › 5. The part worth carrying]])
- View-source and inspect-element disagree exactly when the content is assembled: view-source shows what the server sent, the inspector shows what the browser built. ([[raw/website/projects/kickstarter-scraper#5. The part worth carrying|website/projects/kickstarter-scraper.md › 5. The part worth carrying]])

## Related notes
- [[University of Notre Dame]] — An individual extra-credit project for ITAO 40450 at the Mendoza College of Business (Spring 2023); listed as related work on the Notre Dame entry.
- [[Formula 1 Racing Trends]] — Same course (ITAO 40450), scraped three days later; that archive arrived complete, so it was rate-limited with polite::bow() instead of snapshotted in a browser.

## Sources
- [[raw/website/projects/kickstarter-scraper|Personal website - projects: Kickstarter Scraper]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/kickstarter-scraper.md)
