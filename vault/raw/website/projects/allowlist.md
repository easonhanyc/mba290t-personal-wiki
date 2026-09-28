---
title: "Allowlist — Data Access Management App"
description: "Replacing a freely editable shared spreadsheet — the one governing who could see whose data — with a constrained, logged application."
summary: "Exceptions to sellers' data access lived in a spreadsheet anyone could edit, with no record of who changed what. Allowlist replaced it with a constrained application: read everything, add, remove — but never edit in place, and every action logged."
role: "Builder and product owner · AWS Global Sales Strategy & Analytics"
period: "2023–2026"
depth: "project"
org: "Amazon Web Services"
badges: ["Data governance"]
live: false
tags: ["product", "eng"]
metrics:
  - n: "200+"
    l: "data owners and ops partners"
  - n: "0"
    l: "in-place edits permitted"
  - n: "Every action"
    l: "logged"
links: {}
featured: false
order: 5
---

**Built with:** spec-driven development in the Kiro agentic IDE

<aside class="note"><strong>Confidentiality note.</strong> Written at the level of detail already public on my resume. No schema, field definitions, access rules or record contents appear here.</aside>

> **The 30-second version.** Sellers see data for the territories and accounts they are assigned. The exceptions to that — the overrides and one-off extensions — were being managed in a shared spreadsheet that anyone could open and edit. I replaced it with **Allowlist**: a central application where everyone can read every record and submit or withdraw one, nobody outside admin can alter an existing record, and every action is written to a log.

---

## 1. The thing that was actually broken

Access starts from a baseline. A seller is assigned territories or accounts, and sees the data for those.

The baseline is not the problem. The **exceptions** are, and there are always exceptions:

- A **permanent override** — a manager delegates something above the seller's normal scope, and they need the data that comes with it.
- A **one-time need** — a special initiative requires a wider view for as long as it runs.

Both are legitimate. Both have to be recorded somewhere. And that somewhere was a shared spreadsheet with edit access for everyone who needed to use it.

**The risk is not that the spreadsheet was inaccurate.** It was probably mostly accurate. The risk is that it was *unaccountable*: any row could be changed by anyone at any time, and afterwards there was no way to establish who had changed it, when, or what it had said before. A spreadsheet governing data access is an access-control system in which the controls are a social convention.

That is the failure mode worth naming, because it doesn't look like a failure until it matters. Nothing is visibly wrong. There is simply no answer available to the question "why does this person have this access," and no way to get one.

## 2. What replaced it

<figure class="dg">
<div class="dgscroll">
<svg viewBox="0 0 700 214" role="img" aria-labelledby="al-t" xmlns="http://www.w3.org/2000/svg">
 <title id="al-t">A shared spreadsheet where anyone edits any row, replaced by an application permitting read, add and remove but never in-place edits, with every action logged</title>
 <defs>
  <marker id="al-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="var(--border-strong)"/>
  </marker>
 </defs>
 <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace">
  <rect x="8" y="26" width="292" height="132" rx="8" fill="var(--surface)" stroke="var(--border-strong)"/>
  <text x="154" y="20" font-size="10" fill="var(--ink-3)" text-anchor="middle">before &#8212; shared spreadsheet</text>
  <text x="26" y="56" font-size="10.5" fill="var(--ink-2)">&#183; anyone edits any row</text>
  <text x="26" y="80" font-size="10.5" fill="var(--ink-2)">&#183; free text, inconsistent names</text>
  <text x="26" y="104" font-size="10.5" fill="var(--ink-2)">&#183; prior state overwritten</text>
  <text x="26" y="128" font-size="10.5" fill="var(--ink-2)">&#183; no record of who, or when</text>
  <text x="26" y="148" font-size="9.5" fill="var(--gold)">&#8220;why does this person have access?&#8221; &#8212; no answer</text>
  <path d="M306 92 L338 92" stroke="var(--border-strong)" stroke-width="1.5" marker-end="url(#al-ar)"/>
  <rect x="346" y="26" width="346" height="132" rx="8" fill="var(--surface)" stroke="var(--accent)"/>
  <text x="519" y="20" font-size="10" fill="var(--accent)" text-anchor="middle">after &#8212; Allowlist</text>
  <text x="364" y="56" font-size="10.5" fill="var(--ink-2)">&#183; read every record</text>
  <text x="364" y="80" font-size="10.5" fill="var(--ink-2)">&#183; submit a record &#183; withdraw a record</text>
  <text x="364" y="104" font-size="10.5" fill="var(--ink)">&#183; no in-place edit outside admin</text>
  <text x="364" y="128" font-size="10.5" fill="var(--ink-2)">&#183; structured form, not free text</text>
  <text x="364" y="148" font-size="9.5" fill="var(--accent)">every action written to a log</text>
  <text x="350" y="188" font-size="10.5" fill="var(--ink-2)" text-anchor="middle">An edit is a deletion and an insertion with the history erased.</text>
  <text x="350" y="204" font-size="10.5" fill="var(--ink-2)" text-anchor="middle">Removing the edit is what makes the log complete.</text>
 </g>
</svg>
</div>
<figcaption>Redrawn for this portfolio. Field definitions and access rules omitted.</figcaption>
</figure>

Allowlist is a central application for the same records, with a deliberately narrow set of things a non-admin can do:

- **Read every record.** Visibility is not the thing being restricted — everyone can see the whole picture, which is what makes the register useful.
- **Submit a record, or withdraw one.** Both through a form.
- **Not alter an existing record.** That capability sits with admin alone.

## 3. Why removing "edit" is the decision

Taking edit away from the people who use a tool most looks like a downgrade. It is the choice I would defend hardest.

**An edit is a deletion and an insertion with the history thrown away.** When a row can be changed in place, the previous state stops existing — and no log can recover what was never written down. Forcing a change to happen as *withdraw, then submit* means the same change now leaves two entries behind it, and the sequence stays reconstructable.

That converts the register from a *statement of the present* into a *record of how the present came about*. For a system governing who can see whose data, the second is the one that answers questions. "Who has this access" is useful. "Who granted it, when, and what did it replace" is the question that actually gets asked, and only the second design can answer it.

The narrowness also makes the remaining permissions safe to hand out widely. Because nobody can quietly change a row, read access can go to everyone without anyone needing to be trusted with the register's integrity.

## 4. The form is a data-quality instrument

The other half of the design is that submissions go through a structured form rather than free-typed cells.

That reads like a user-experience decision and isn't one. It is about the **downstream**: the data team has to process these records, and free text produces typos and names that don't match anything. Reconciling those is real work, and it happens at the point of *processing* — where the person doing it doesn't know what was meant.

A constrained form moves that cost to the point of *entry*, where the person filling it in does know. This is the general shape worth carrying: **validation is cheapest where the intent still exists**. Every step it is deferred, it gets more expensive and less accurate.

It matters more here than it would elsewhere because of who the users are. The 200+ people using Allowlist are data owners and strategy & ops partners — the people sellers bring these requests *to*, not the sellers themselves. The person filling in the form is transcribing somebody else's request, which is exactly the situation in which free text goes wrong.

## 5. The log is the product

Every action on the application, and on the data access it governs, is recorded.

I would argue this is the actual deliverable and the register is the interface to it. The spreadsheet already held the records. What it could not do was tell you how they got there — and that is the entire difference between a list and a control.

An audit trail is also the thing that makes the system cheaper to operate rather than more expensive. Questions about historical access stop requiring an investigation and become a lookup.

## 6. Built spec-first

I built Allowlist end to end through spec-driven development in the Kiro agentic IDE — writing the specification, then having the agent build against it.

The discipline is the same one I would apply without an agent: **the specification comes before the code, and the code is measured against it rather than the other way round.** Writing a PRD before building is the identical habit at a different altitude. What the agentic workflow changes is the cost of being vague — an underspecified requirement produces a confidently wrong implementation immediately, rather than surfacing three weeks later in review. The feedback on specification quality gets much faster, and much less forgiving.
