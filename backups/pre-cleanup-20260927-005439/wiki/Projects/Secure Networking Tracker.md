---
title: Secure Networking Tracker
type: project
summary: The Secure Networking Tracker is a private networking tool designed for users at Berkeley to maintain connections.
sources:
- path: raw/course-projects/secure-networking-tracker/README.md
  source_id: course-projects-secure-networking-tracker-readme-4b2dc6a2
  sha256: 4b2dc6a22bd026b3b7eb9a5e12d96ec59610ce08edf74bf395f9b470d9db0403
- path: raw/course-projects/secure-networking-tracker/docs/how-it-works.md
  source_id: course-projects-secure-networking-tracker-docs-how-it-works-5ab70ce2
  sha256: 5ab70ce209d7786d6c97403a3a50142886337415d7fb572858915c4c4bea7691
- path: raw/website/projects/secure-networking-tracker.md
  source_id: website-projects-secure-networking-tracker-fb399686
  sha256: fb3996868f0d02d7a33649fbff5a97cd7843951c9fb8205cc190d9ae27833838
generated_by: gemma-4-e4b-it-qat-q4_0 (local, llama.cpp llama-server)
generated_at: '2026-09-27T00:54:10'
reviewed: false
---

# Secure Networking Tracker

The Secure Networking Tracker is a private networking tool designed for users at Berkeley to maintain connections. It enforces strict data ownership using Row Level Security in Postgres, ensuring users can only access their own contacts.

## Key facts

### From course-projects/secure-networking-tracker/README.md
- A private networking tracker for the people you want to stay connected with at Berkeley is the Secure Networking Tracker. ([[raw/course-projects/secure-networking-tracker/README#Secure Networking Tracker|course-projects/secure-networking-tracker/README.md › Secure Networking Tracker]])
- Every contact belongs to exactly one account, and that ownership is enforced by Postgres itself through Row Level Security. ([[raw/course-projects/secure-networking-tracker/README#Secure Networking Tracker|course-projects/secure-networking-tracker/README.md › Secure Networking Tracker]])
- The contact list can be viewed as a table on desktop and as stacked cards on mobile. ([[raw/course-projects/secure-networking-tracker/README#Features|course-projects/secure-networking-tracker/README.md › Features]])
- Priority is a closed set — high, medium, low — enforced in the API and as a Postgres enum. ([[raw/course-projects/secure-networking-tracker/README#Features|course-projects/secure-networking-tracker/README.md › Features]])
- Contacts persist in Neon Postgres and survive a refresh, a new tab, or a new device. ([[raw/course-projects/secure-networking-tracker/README#Features|course-projects/secure-networking-tracker/README.md › Features]])
- The architecture involves React client components fetching data from Next.js Route Handlers, which then interact with the Neon Data API. ([[raw/course-projects/secure-networking-tracker/README#Architecture|course-projects/secure-networking-tracker/README.md › Architecture]])
- The frontend bundle contains no database URL, no service key and no auth secret. ([[raw/course-projects/secure-networking-tracker/README#Architecture|course-projects/secure-networking-tracker/README.md › Architecture]])
- The project uses Next.js 16 (App Router) as its framework. ([[raw/course-projects/secure-networking-tracker/README#Technology stack|course-projects/secure-networking-tracker/README.md › Technology stack]])
- Prerequisites for local setup include Node.js 20+ and a free Neon account. ([[raw/course-projects/secure-networking-tracker/README#Local setup|course-projects/secure-networking-tracker/README.md › Local setup]])
- The Neon Console must have Auth (Managed Better Auth) and the Data API enabled on the project. ([[raw/course-projects/secure-networking-tracker/README#Local setup|course-projects/secure-networking-tracker/README.md › Local setup]])
- The rule is that a row belongs to the user whose JWT created it, and only that user can read or change it. ([[raw/course-projects/secure-networking-tracker/README#Authentication and ownership|course-projects/secure-networking-tracker/README.md › Authentication and ownership]])
- Row Level Security is enabled and forced on contacts with four separate policies for authenticated users. ([[raw/course-projects/secure-networking-tracker/README#Authentication and ownership|course-projects/secure-networking-tracker/README.md › Authentication and ownership]])

### From course-projects/secure-networking-tracker/docs/how-it-works.md
- A signed-in user gets a private list of contacts, and the browser never talks to the database. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#1. The one-paragraph version|course-projects/secure-networking-tracker/docs/how-it-works.md › 1. The one-paragraph version]])
- The `user_id` column in the `public.contacts` table is of type `text` and serves as the whole security model. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#2. The schema|course-projects/secure-networking-tracker/docs/how-it-works.md › 2. The schema]])
- The ownership rule states that a row belongs to whoever's JWT created it, and only that user can read or change it. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#3. The ownership rule|course-projects/secure-networking-tracker/docs/how-it-works.md › 3. The ownership rule]])
- Layer 1 assigns ownership because the API never sends `user_id`, and the value can only come from the verified token. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#Layer 1 — the database assigns ownership|course-projects/secure-networking-tracker/docs/how-it-works.md › Layer 1 — the database assigns ownership]])
- Layer 2 uses Row Level Security policies to filter every statement for the `authenticated` role. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#Layer 2 — Row Level Security filters every statement|course-projects/secure-networking-tracker/docs/how-it-works.md › Layer 2 — Row Level Security filters every statement]])
- The distinction between `USING` and `WITH CHECK` is that `USING` filters existing rows, while `WITH CHECK` inspects the row as it will be after the write. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#Layer 2 — Row Level Security filters every statement|course-projects/secure-networking-tracker/docs/how-it-works.md › Layer 2 — Row Level Security filters every statement]])
- Layer 3 involves the application checking routes and returning 401s, which is defense in depth but not the primary security mechanism. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#Layer 3 — the application checks too|course-projects/secure-networking-tracker/docs/how-it-works.md › Layer 3 — the application checks too]])
- When editing a contact, the request goes from the browser to the route handler, then to Neon Auth for a JWT, and finally to Postgres. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#4. What happens on one request|course-projects/secure-networking-tracker/docs/how-it-works.md › 4. What happens on one request]])
- Returning 404 instead of 403 when a row is not owned is because RLS makes the row invisible, not forbidden. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#4. What happens on one request|course-projects/secure-networking-tracker/docs/how-it-works.md › 4. What happens on one request]])
- Validation happens three times: in the browser form, in the route handler using Zod, and via Postgres CHECK constraints. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#5. Validation happens three times, on purpose|course-projects/secure-networking-tracker/docs/how-it-works.md › 5. Validation happens three times, on purpose]])
- The `NEXT_PUBLIC_` endpoints are safe to expose because Row Level Security is doing the work. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works|course-projects/secure-networking-tracker/docs/how-it-works.md › 6. Secrets: what is public and why that's fine]])
- Going through the backend API adds an independent layer of trusted validation and controlled error messages, even if RLS protects the data. ([[raw/course-projects/secure-networking-tracker/docs/how-it-works#7. Questions you should have an answer for|course-projects/secure-networking-tracker/docs/how-it-works.md › 7. Questions you should have an answer for]])

### From website/projects/secure-networking-tracker.md
- The Secure Networking Tracker is a private contact tracker where ownership is enforced by Postgres itself, not by the API layer. ([[raw/website/projects/secure-networking-tracker|website/projects/secure-networking-tracker.md › front matter]])
- The project is a networking tracker for Berkeley contacts where one user's list is unreachable to another even if the API layer were bypassed entirely — because the boundary lives in Postgres, not in application code. ([[raw/website/projects/secure-networking-tracker|website/projects/secure-networking-tracker.md › front matter]])
- The stack used for the project includes Next.js 16, Neon Postgres, Better Auth, and Vercel. ([[raw/website/projects/secure-networking-tracker|website/projects/secure-networking-tracker.md]])
- The interesting part of the tracker is where the ownership boundary sits, as every contact belongs to exactly one account, and Postgres enforces that below the application through Row Level Security. ([[raw/website/projects/secure-networking-tracker|website/projects/secure-networking-tracker.md]])
- Three independent mechanisms enforce one rule: a row belongs to the user whose token created it. ([[raw/website/projects/secure-networking-tracker#2. Where the boundary actually is|website/projects/secure-networking-tracker.md › 2. Where the boundary actually is]])
- The database assigns ownership by setting user_id to NOT NULL DEFAULT auth.user_id(), ensuring the value always comes from the verified token. ([[raw/website/projects/secure-networking-tracker#2. Where the boundary actually is|website/projects/secure-networking-tracker.md › 2. Where the boundary actually is]])
- RLS filters every statement using four policies for authenticated users covering select, insert, update and delete. ([[raw/website/projects/secure-networking-tracker#2. Where the boundary actually is|website/projects/secure-networking-tracker.md › 2. Where the boundary actually is]])
- A consequence of using RLS is that PATCH or DELETE against another user's contact returns 404, not 403, because the row is invisible to the caller. ([[raw/website/projects/secure-networking-tracker#The subtle one|website/projects/secure-networking-tracker.md › The subtle one]])
- The claim that no secret reaches the browser is verified by checking the actual production build for secrets like NEON_AUTH_COOKIE_SECRET and DATABASE_URL. ([[raw/website/projects/secure-networking-tracker#3. Verified, not asserted|website/projects/secure-networking-tracker.md › 3. Verified, not asserted]])
- 28 tests cover the trusted validation module, asserting that a client-supplied user_id is stripped and unknown sort parameters fall back to safe defaults. ([[raw/website/projects/secure-networking-tracker#3. Verified, not asserted|website/projects/secure-networking-tracker.md › 3. Verified, not asserted]])
- One thing that could be done differently is implementing keyset pagination instead of loading every matching row. ([[raw/website/projects/secure-networking-tracker#4. What I'd do differently|website/projects/secure-networking-tracker.md › 4. What I'd do differently]])
- The current search functionality uses ILIKE, which is substring matching with no ranking or typo tolerance. ([[raw/website/projects/secure-networking-tracker#4. What I'd do differently|website/projects/secure-networking-tracker.md › 4. What I'd do differently]])

## Related notes
- [[UC Berkeley Haas MBA MEng]] — Both notes are associated with UC Berkeley.
- [[Ms. Pac-Man DQN Implementation]] — Both projects involve implementing and training an agent using a Deep Q-Network.
- [[Pac-Man DQN Methodology Study]] — Both notes relate to the methodology and implementation of a DQN agent for Ms. Pac-Man.

## Sources
- [[raw/course-projects/secure-networking-tracker/README|MBA 290T project - Secure Networking Tracker (Assignment 1): Secure Networking Tracker]] — [origin](https://github.com/easonhanyc/secure-networking-tracker/blob/2aa3c1e478b0ef74f03f9c5859c9f5ab8a38ce0f/README.md)
- [[raw/course-projects/secure-networking-tracker/docs/how-it-works|MBA 290T project - Secure Networking Tracker (Assignment 1): How this app works]] — [origin](https://github.com/easonhanyc/secure-networking-tracker/blob/2aa3c1e478b0ef74f03f9c5859c9f5ab8a38ce0f/docs/how-it-works.md)
- [[raw/website/projects/secure-networking-tracker|Personal website - projects: Secure Networking Tracker]] — [origin](https://github.com/easonhanyc/easonhanyc.github.io/blob/e8ea53c3546621c79620bbfa04bd88321fac8ec3/src/content/projects/secure-networking-tracker.md)
