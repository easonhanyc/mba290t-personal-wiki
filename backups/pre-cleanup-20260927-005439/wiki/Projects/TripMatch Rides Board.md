---
title: TripMatch Rides Board
type: project
summary: TripMatch was a verified, Berkeley-only rides board designed to solve the problem of unstructured ride coordination in group chats.
sources:
- path: raw/website/projects/tripmatch.md
  source_id: website-projects-tripmatch-c8542a2c
  sha256: c8542a2ca92bca393a12e43886bbd9c6d2b9afd13bf258d4ccd15f7e9ee82adf
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# TripMatch Rides Board

TripMatch was a verified, Berkeley-only rides board designed to solve the problem of unstructured ride coordination in group chats. The project evolved from a simple prototype to a robust system using a GitHub Pages, Cloudflare Worker, and D1 architecture.

## Key facts
- A 400-person class coordinates rides by scrolling a WhatsApp chat, where requests get buried and matching seats go unused. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › front matter]])
- The project was a verified, Berkeley-only rides board. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › front matter]])
- The timeline for the project was August 22–27, 2026. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md]])
- The problem was that ride coordination lived in an unstructured group chat, and matches were found by luck, not by search. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md]])
- Three costs of using the WhatsApp chat were that requests get buried, there is no way to see overlap, and the failure mode is silent waste. ([[raw/website/projects/tripmatch#1. The problem, and why it wasn't already solved|website/projects/tripmatch.md › 1. The problem, and why it wasn't already solved]])
- The project was scoped to replace a group chat's search function for approximately 400 people who already know each other. ([[raw/website/projects/tripmatch#1. The problem, and why it wasn't already solved|website/projects/tripmatch.md › 1. The problem, and why it wasn't already solved]])
- The PRD's non-goals included not being a payments/cost-splitting tool, not real-time dispatch, not a WhatsApp replacement, no public/open matching, and no native mobile app. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 2. What I deliberately chose *not* to build]])
- Three gaps surfaced within days of V1 going to a slice of the class, leading to the implementation of owner-scoped delete, an edit control, and date chips for better volume scaling. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 3. From prototype to launch: what real users changed]])
- V1 stored the whole board as one JSON document in a hosted-JSON service. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 4. The launch-hardening call: killing my own v1 architecture]])
- Against the expected load of ~400 students and ~200 concurrent posts, V1 had three defects. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 4. The launch-hardening call: killing my own v1 architecture]])
- The second defect involved simultaneous posts silently overwriting each other because two people acting inside one HTTP round trip meant one post vanished. ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 4. The launch-hardening call: killing my own v1 architecture]])
- The rebuilt storage layer behind an API used the architecture: GitHub Pages (static) → Cloudflare Worker → D1 (SQLite). ([[raw/website/projects/tripmatch|website/projects/tripmatch.md › 4. The launch-hardening call: killing my own v1 architecture]])

## Related notes
- [[Secure Networking Tracker]] — Both projects involve tools designed for the Berkeley community.
- [[UC Berkeley Haas MBA MEng]] — This note describes a project from a program at UC Berkeley.

## Sources
- [[raw/website/projects/tripmatch|Personal website - projects: TripMatch]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/tripmatch.md)
