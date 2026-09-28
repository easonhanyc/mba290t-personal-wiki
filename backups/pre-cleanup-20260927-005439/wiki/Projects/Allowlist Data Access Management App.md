---
title: Allowlist Data Access Management App
type: project
summary: Allowlist is a constrained application built to replace a shared spreadsheet that governed data access exceptions.
sources:
- path: raw/website/projects/allowlist.md
  source_id: website-projects-allowlist-4567a2ef
  sha256: 4567a2efe10e069437f63093bd3c35d50f33bb426a0103939f09430fd09b2c73
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Allowlist Data Access Management App

Allowlist is a constrained application built to replace a shared spreadsheet that governed data access exceptions. It allows users to read all records and submit or withdraw records, but prevents in-place edits, ensuring every action is logged. This design transforms the register from a statement of the present into a record of how the present came about.

## Key facts
- Allowlist replaced a freely editable shared spreadsheet that governed who could see whose data with a constrained, logged application. ([[raw/website/projects/allowlist|website/projects/allowlist.md › front matter]])
- Sellers see data for the territories and accounts they are assigned, and exceptions to that are managed in a shared spreadsheet that anyone could open and edit. ([[raw/website/projects/allowlist|website/projects/allowlist.md]])
- The risk with the spreadsheet was that it was unaccountable because any row could be changed by anyone at any time with no way to establish who changed it, when, or what it had said before. ([[raw/website/projects/allowlist#1. The thing that was actually broken|website/projects/allowlist.md › 1. The thing that was actually broken]])
- Allowlist is a central application for the same records, with a deliberately narrow set of things a non-admin can do: Read every record, Submit a record, or withdraw one. ([[raw/website/projects/allowlist#2. What replaced it|website/projects/allowlist.md › 2. What replaced it]])
- Forcing a change to happen as withdraw, then submit means the same change leaves two entries behind, and the sequence stays reconstructable. ([[raw/website/projects/allowlist|website/projects/allowlist.md › 3. Why removing "edit" is the decision]])
- A constrained form moves the cost of data quality to the point of entry, where the person filling it in knows what was meant. ([[raw/website/projects/allowlist#4. The form is a data-quality instrument|website/projects/allowlist.md › 4. The form is a data-quality instrument]])
- Every action on the application, and on the data access it governs, is recorded. ([[raw/website/projects/allowlist#5. The log is the product|website/projects/allowlist.md › 5. The log is the product]])
- Allowlist was built end to end through spec-driven development in the Kiro agentic IDE. ([[raw/website/projects/allowlist#6. Built spec-first|website/projects/allowlist.md › 6. Built spec-first]])

## Related notes
- [[Amazon Web Services Role]] — Both notes relate to building and managing internal products for large organizations.
- [[Action Hub Ranked Alerts]] — Both projects involve building applications to replace manual, unconstrained processes.
- [[Pull-Request Automation Skill]] — Both projects involve building internal tools to automate processes.

## Sources
- [[raw/website/projects/allowlist|Personal website - projects: Allowlist — Data Access Management App]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/allowlist.md)
