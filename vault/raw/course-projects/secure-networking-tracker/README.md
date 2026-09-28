# Secure Networking Tracker

A private networking tracker for the people you want to stay connected with at Berkeley. Sign up, add the people you meet — where you met them, what they do, how much you want to prioritise the relationship, and what you talked about — then sort, filter and search that list as it grows. Every contact belongs to exactly one account, and that ownership is enforced by Postgres itself through Row Level Security, so one user's list is unreachable to another even if the API layer were bypassed entirely.

**Live app:** **<https://secure-networking-tracker-phi.vercel.app>**

---

## Contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Technology stack](#technology-stack)
- [Architecture](#architecture)
- [Local setup](#local-setup)
- [Environment variables](#environment-variables)
- [Database schema](#database-schema)
- [Authentication and ownership](#authentication-and-ownership)
- [Testing](#testing)
- [Deployment](#deployment)
- [Grading evidence](#grading-evidence)
- [Secret hygiene](#secret-hygiene)
- [How it works, in depth](docs/how-it-works.md)
- [Known limitations and what I would do next](#known-limitations-and-what-i-would-do-next)

---

## Screenshots

All captured from the deployed application by `npm run screenshots`, which drives the real app in Chrome.

### Sign in

![Sign-in page](docs/screenshots/01-sign-in.png)

### First run — the empty state

![Empty state](docs/screenshots/02-empty-state.png)

### Invalid input fails safely

A name of only spaces is sent to the server, rejected there, and the reason comes back per field. The browser form does not block it — the message shown is the one the API returned.

![Invalid input rejected by the server](docs/screenshots/03-invalid-input.png)

### The contact list

![Contact list](docs/screenshots/04-contact-list.png)

### Adding and editing

![Edit contact](docs/screenshots/05-edit-contact.png)

### Filtering by priority

![Filtered to high priority](docs/screenshots/06-filter-priority.png)

### Sorting by name

![Sorted by name](docs/screenshots/07-sort-by-name.png)

### Data survives a refresh

The same rows after a full page reload — they are read back from Neon Postgres, not from browser state.

![After a refresh](docs/screenshots/08-after-refresh.png)

### After deleting a contact

![After delete](docs/screenshots/10-after-delete.png)

### Two accounts, side by side

Two users signed in at once against the same database and the same `contacts` table. User A owns three contacts; User B, signed in and looking at the same table, sees none of them. The strip underneath records what User B got when asking the API directly for one of A's rows by id.

![Two-account isolation](docs/screenshots/12-two-account-isolation.png)

### Mobile

The table becomes stacked cards below `md`; the toolbar wraps to full-width controls.

<img src="docs/screenshots/09-mobile.png" alt="Mobile layout" width="320">

### Signed out

Signing out clears the session and returns to sign-in. Visiting `/contacts` afterwards redirects back here.

![Signed out](docs/screenshots/11-signed-out.png)

---

## Features

**Accounts**
- Email + password sign-up and sign-in via Neon Managed Better Auth
- Sign out from the app header
- Signed-out visitors are redirected to sign-in; signed-in visitors land on their contacts

**Contacts**
- Add a contact with name, company, role, where you met, notes and priority
- Priority is a closed set — `high`, `medium`, `low` — enforced in the API *and* as a Postgres enum
- View contacts as a table on desktop and as stacked cards on mobile
- Edit and delete your own contacts
- Sort by date added, name, company or priority, ascending or descending
- Filter by priority, and search across name, company, role and where you met
- Contacts persist in Neon Postgres and survive a refresh, a new tab, or a new device

**Interface states**
- Loading: skeleton placeholders while a query is in flight
- Empty: distinct messages for "no contacts yet" and "nothing matches these filters", each with the useful next action
- Success: toast confirmations for add, edit and delete
- Error: an inline alert with a retry button for failed loads; per-field messages for rejected input
- Responsive from a 320px phone up to a wide desktop

---

## Technology stack

| Layer | Choice | Why |
|---|---|---|
| Framework | **Next.js 16** (App Router) | One project with a genuine server/client split. Server Components and Route Handlers run on the server, so secrets and trusted logic are never sent to the browser. |
| Language | **TypeScript** (strict) | The contact shape is defined once and shared by the API, the browser client and the tests, so a mismatch is a compile error rather than a runtime bug. |
| Styling | **Tailwind CSS v4 + shadcn/ui** (Radix primitives) | A real component system rather than ad-hoc CSS: accessible dialogs, selects and menus out of the box, with consistent tokens for light and dark. |
| Validation | **Zod** | One schema drives server validation, TypeScript types and test assertions. |
| Database | **Neon Postgres** | Serverless Postgres, so RLS — the security model this assignment is built around — is available natively. |
| Auth | **Neon Managed Better Auth** | Issues the JWT that Postgres reads via `auth.user_id()`, tying sessions directly to row ownership. |
| Data access | **Neon Data API** via `@neondatabase/neon-js` | A PostgREST-style API that honours the caller's JWT, so RLS applies to every query. |
| Tests | **Vitest** | Fast, zero-config, clear output. |
| Hosting | **Vercel** | First-class Next.js support and per-environment secrets. |
| Source control | **Git + GitHub** | |

---

## Architecture

```
Browser (React client components)
  │   fetch('/api/contacts')  — no database URL, no tokens, no DB credentials
  ▼
Next.js Route Handlers + Server Actions        ← the backend, server-only
  │   1. Read the session from an httpOnly cookie
  │   2. Validate the request body with Zod  (src/lib/validation/contact.ts)
  │   3. Mint a short-lived JWT for this user from Neon Auth
  ▼
Neon Data API  (Authorization: Bearer <user JWT>)
  ▼
Neon Postgres — Row Level Security evaluates auth.user_id() per row
```

**Frontend.** React client components under `src/components`. They render state and collect input; they hold no business rules. The browser bundle contains no database URL, no service key and no auth secret — it only ever calls same-origin `/api/*` routes.

**Backend.** Route Handlers in `src/app/api` and Server Actions in `src/lib/auth/actions.ts`. Every request is re-validated here regardless of what the form already checked. Sign-in and sign-up are Server Actions, so credentials are posted to our own origin and exchanged with Neon server-side; the session lands in an httpOnly cookie the browser's JavaScript cannot read.

**Why route handlers instead of calling the Data API from the browser.** Neon's Data API is safe to call directly because RLS protects the rows, and this project could have done that. Going through our own backend adds a second, independent layer: input is validated by trusted code before it reaches the database, error messages are normalised so raw Postgres text never reaches the client, and the query shape stays under our control. RLS remains the actual security boundary — the API layer is defence in depth, not a substitute.

### How the Neon client is constructed

`@neondatabase/neon-js` offers two shapes. The two-URL object form gives you an auth client and a data client together, and is what you want when the **browser** drives both:

```ts
createClient({
  auth:    { url: NEXT_PUBLIC_NEON_AUTH_URL },
  dataApi: { url: NEXT_PUBLIC_NEON_DATA_API_URL },
});
```

This project uses the token-provider form instead, because authentication is already handled server-side by `@neondatabase/auth` and the session lives in an httpOnly cookie the browser cannot read:

```ts
createClient({
  dataApi: {
    url: NEXT_PUBLIC_NEON_DATA_API_URL,
    getToken: async () => /* JWT for the signed-in user, minted server-side */,
  },
});
```

Both endpoints are still used, and both are still declared as `NEXT_PUBLIC_*`: the auth URL configures `createNeonAuth` in `src/lib/auth/server.ts`, and the data URL configures the client above in `src/lib/db/server.ts`. What changes is only *where* the two are wired together — on the server, rather than in the browser.

The reason is the trust boundary. With the two-URL form in the browser, the client holds its own session and calls the Data API directly; validation then has to live entirely in database constraints, because there is no server in the path to run it. Minting the token server-side keeps a trusted checkpoint in front of every write — Zod runs there — while RLS still does the actual access control underneath. The database-side rules are in place either way; this adds a layer rather than replacing one.

**Database.** A single `contacts` table with Row Level Security enabled and four ownership policies. Sorting, filtering and searching are pushed down to Postgres rather than done in the browser, so the database returns only the rows the screen needs.

**Authentication.** Neon Managed Better Auth. The server exchanges the session for a JWT on each data request and passes it to the Data API, so Postgres evaluates `auth.user_id()` as the signed-in user.

**Hosting.** Vercel. Public endpoints are set as `NEXT_PUBLIC_*`; the cookie secret and `DATABASE_URL` are server-only environment variables.

### Where things live

```
db/schema.sql                       Table, constraints, indexes, RLS policies, grants
scripts/apply-schema.mjs            Applies schema.sql via DATABASE_URL (npm run db:push)
scripts/privacy-check.mjs           End-to-end two-account privacy test (npm run test:privacy)
src/app/api/auth/[...path]/route.ts Neon Auth endpoints
src/app/api/contacts/route.ts       GET list (sort/filter/search), POST create
src/app/api/contacts/[id]/route.ts  PATCH update, DELETE
src/app/(auth)/sign-in, sign-up     Auth pages
src/app/contacts/page.tsx           Main screen (server-guarded)
src/lib/auth/server.ts              Neon Auth instance; the only reader of the cookie secret
src/lib/auth/actions.ts             Sign-up / sign-in / sign-out server actions
src/lib/db/server.ts                Data API client bound to the caller's JWT
src/lib/validation/contact.ts       Trusted validation rules (the tested module)
src/lib/env.ts                      Public vs server-only environment split
tests/contact-validation.test.ts    Automated validation tests
```

---

## Local setup

**Prerequisites:** Node.js 20+ and a free [Neon](https://neon.com) account.

```bash
git clone https://github.com/easonhanyc/secure-networking-tracker.git
cd secure-networking-tracker
npm install
```

**1. Create the Neon project.** In the Neon Console create a project, then enable **Auth** (Managed Better Auth) and the **Data API** on it. Copy three values:

- the **Auth URL** → `NEXT_PUBLIC_NEON_AUTH_URL`
- the **Data API URL** → `NEXT_PUBLIC_NEON_DATA_API_URL`
- the **Postgres connection string** → `DATABASE_URL`

**2. Configure the environment.**

```bash
cp .env.example .env.local
```

Fill in the three values above, then generate the cookie secret:

```bash
openssl rand -base64 32
```

and put it in `NEON_AUTH_COOKIE_SECRET`. `.env.local` is gitignored.

**3. Create the table and security policies.**

```bash
npm run db:push
```

This applies `db/schema.sql` and prints the RLS policies it created, so you can see the four ownership policies exist before starting the app.

**4. Run it.**

```bash
npm run dev
```

Open <http://localhost:3000>. Localhost is trusted by Neon Auth by default, so no extra configuration is needed to sign in locally — deployed domains do need to be added, see [Deployment](#deployment).

### All commands

| Command | What it does |
|---|---|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm start` | Serve the production build |
| `npm test` | Automated validation tests (Vitest) |
| `npm run typecheck` | TypeScript, no emit |
| `npm run lint` | ESLint |
| `npm run db:push` | Apply `db/schema.sql` and print the RLS policies |
| `npm run test:privacy` | Two-account privacy check against a running app |
| `npm run screenshots` | Recapture the README screenshots by driving the app in Chrome |
| `npm run screenshots:isolation` | Capture the two-account isolation image |
| `npm run cleanup:test-accounts` | Remove throwaway accounts left by the two scripts above (add `-- --yes` to apply) |

---

## Environment variables

`.env.example` is committed with placeholder values only. `.env.local` holds the real values and is gitignored.

| Variable | Exposed to browser | Purpose |
|---|---|---|
| `NEXT_PUBLIC_NEON_AUTH_URL` | Yes | HTTPS Neon Auth endpoint |
| `NEXT_PUBLIC_NEON_DATA_API_URL` | Yes | HTTPS Neon Data API endpoint |
| `NEON_AUTH_COOKIE_SECRET` | **No** | Signs the session cookie. 32+ characters. |
| `NEON_AUTH_BASE_URL` | **No** | Optional. Defaults to the public auth URL. |
| `DATABASE_URL` | **No** | Postgres connection string. Used **only** by `npm run db:push` from a developer machine — the running application never reads it. |

The two `NEXT_PUBLIC_*` values are HTTPS endpoints, not secrets. They are useless without a valid JWT, because Row Level Security is what actually protects the rows. The cookie secret and the connection string never leave the server and are never committed.

---

## Database schema

`public.contacts`:

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | `bigint` | primary key, generated by default as identity | |
| `user_id` | `text` | **not null**, `DEFAULT auth.user_id()` | Owner. Set by Postgres from the JWT, never sent by the client. |
| `name` | `text` | not null, `CHECK (length(btrim(name)) > 0)`, `CHECK (length(name) <= 120)` | Blank names are impossible to store. |
| `company` | `text` | nullable | |
| `role` | `text` | nullable | |
| `where_met` | `text` | nullable | |
| `notes` | `text` | nullable | |
| `priority` | `contact_priority` | not null, default `'medium'` | Enum: `high`, `medium`, `low`. |
| `created_at` | `timestamptz` | not null, default `now()` | |
| `updated_at` | `timestamptz` | not null, default `now()` | Maintained by a `BEFORE UPDATE` trigger. |

Also created:

- `contact_priority` — a Postgres enum, so an invalid priority is rejected by the database as well as by the API.
- `contacts_user_id_created_at_idx` on `(user_id, created_at DESC)` — every query is "my contacts, ordered by…", so the index leads with the owner.
- `contacts_set_updated_at` — a `BEFORE UPDATE` trigger that refreshes `updated_at` and **pins `user_id` to its previous value**, so a row can never be re-parented on update.

Because `priority` is an enum, sorting by it uses declaration order (`high`, `medium`, `low`) rather than alphabetical — ascending puts the people you care most about first.

---

## Authentication and ownership

**The rule:** a row belongs to the user whose JWT created it, and only that user can read or change it.

Three independent mechanisms enforce it:

**1. The database assigns ownership.** `user_id` is `NOT NULL DEFAULT auth.user_id()`. The API never sends `user_id` — the Zod schema strips it if a client tries — so the value always comes from the verified token.

**2. Row Level Security filters every statement.** RLS is enabled *and forced* on `contacts`, with four separate policies for `authenticated`:

```sql
CREATE POLICY contacts_select_own ON public.contacts
  FOR SELECT TO authenticated
  USING ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_insert_own ON public.contacts
  FOR INSERT TO authenticated
  WITH CHECK ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_update_own ON public.contacts
  FOR UPDATE TO authenticated
  USING ((SELECT auth.user_id()) = user_id)
  WITH CHECK ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_delete_own ON public.contacts
  FOR DELETE TO authenticated
  USING ((SELECT auth.user_id()) = user_id);
```

`USING` decides which rows a statement may *see or target*; `WITH CHECK` decides what a row is allowed to *look like afterwards*. The update policy needs both: without `WITH CHECK`, a user could edit a row they own and set `user_id` to someone else's id — handing the row away, or planting a row in another user's list. `WITH CHECK` makes that fail, and the `BEFORE UPDATE` trigger blocks it a second time. The `anon` role is granted nothing on the table.

**3. The application layer checks too.** Route handlers reject unauthenticated requests with 401 before touching the database, and the contacts page redirects signed-out visitors. This is convenience and defence in depth — it is not what makes the data private.

A consequence worth noting: `PATCH`/`DELETE` on someone else's contact id returns **404, not 403**. The row is invisible under RLS, so from the caller's point of view it does not exist — which also avoids confirming that a given id exists at all.

For a fuller walkthrough — `USING` vs `WITH CHECK`, why the update policy needs both, why deleting someone else's contact returns 404, and where validation happens — see **[docs/how-it-works.md](docs/how-it-works.md)**.

**Request flow for "edit a contact":** browser `PATCH /api/contacts/42` → route handler reads the httpOnly session cookie → 401 if absent → Zod validates the body and drops any `user_id` → the server mints a JWT for this user from Neon Auth → the Data API is called with that JWT → Postgres applies `contacts_update_own` → if the row is not the caller's, zero rows update and the handler returns 404.

---

## Testing

### Automated tests

```bash
npm test
```

`tests/contact-validation.test.ts` covers `src/lib/validation/contact.ts` — the module the route handlers call on every write, i.e. the trusted validation, not the browser form. 28 tests assert that:

- a complete, valid contact is accepted, and each of `high`/`medium`/`low` is accepted
- an empty, whitespace-only, missing, or over-long name is rejected with `"Name is required."`
- invalid priorities (`urgent`, `HIGH`, `""`, `1`, `null`, `undefined`) are rejected with a clear message
- whitespace is trimmed and blank optional fields become `null` rather than `""`
- a client-supplied `user_id` is stripped, so ownership cannot be forged through the API
- a non-object body (`null`, a string, a number) is rejected instead of crashing
- partial updates work, empty updates are rejected, and a name cannot be blanked out
- unknown `sort` and `priority` query parameters fall back to safe defaults instead of being passed through to the database
- an over-long search term is truncated, and `%`, `_` and `\` in a search term are escaped so a user cannot alter the match pattern

```
$ npm test

 RUN  v4.1.11

 ✓ tests/contact-validation.test.ts > validateContactCreate > accepts a complete, valid contact 3ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects an empty name with a clear message 1ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects a whitespace-only name 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects a missing name 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects a name longer than 120 characters 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority "urgent" 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority "HIGH" 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority "" 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority "1" 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority null 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects the invalid priority undefined 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > accepts the valid priority high 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > accepts the valid priority medium 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > accepts the valid priority low 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > trims surrounding whitespace and normalises blank optional fields to null 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > ignores a client-supplied user_id so ownership cannot be forged 0ms
 ✓ tests/contact-validation.test.ts > validateContactCreate > rejects a non-object body 0ms
 ✓ tests/contact-validation.test.ts > validateContactUpdate > accepts a partial update 1ms
 ✓ tests/contact-validation.test.ts > validateContactUpdate > rejects an empty update 0ms
 ✓ tests/contact-validation.test.ts > validateContactUpdate > rejects an invalid priority on update 0ms
 ✓ tests/contact-validation.test.ts > validateContactUpdate > rejects blanking out the name 0ms
 ✓ tests/contact-validation.test.ts > parseListQuery > falls back to safe defaults when parameters are absent 1ms
 ✓ tests/contact-validation.test.ts > parseListQuery > ignores an unknown sort column instead of passing it through 0ms
 ✓ tests/contact-validation.test.ts > parseListQuery > ignores an unknown priority filter 0ms
 ✓ tests/contact-validation.test.ts > parseListQuery > reads valid parameters 0ms
 ✓ tests/contact-validation.test.ts > parseListQuery > caps an over-long search term 1ms
 ✓ tests/contact-validation.test.ts > escapeLikePattern > escapes wildcards so a search term cannot alter the match pattern 0ms
 ✓ tests/contact-validation.test.ts > escapeLikePattern > leaves ordinary text untouched 0ms

 Test Files  1 passed (1)
      Tests  28 passed (28)
   Duration  227ms
```

### Two-account privacy check

```bash
npm run test:privacy                        # against http://localhost:3000
npm run test:privacy -- https://your.app    # against the deployed app
```

`npm run screenshots:isolation` captures the same result visually — the side-by-side image above.

Both scripts create throwaway accounts. `npm run cleanup:test-accounts -- --yes` removes them again, and only touches emails matching the generated test patterns.

`scripts/privacy-check.mjs` drives the real HTTP API end to end: it signs up two throwaway accounts, has User A create a contact, then has User B attempt to list, edit, re-parent and delete it, and finally checks that a signed-out client is rejected and that A's row is untouched. It exercises the whole stack — route handlers, the Data API, and the RLS policies in Postgres.

Run against the deployed application:

```
$ npm run test:privacy -- https://secure-networking-tracker-phi.vercel.app

Two-account privacy check against https://secure-networking-tracker-phi.vercel.app

Signed up privacy-a-1788840511281@example.com and privacy-b-1788840511281@example.com

User A
  ✔ can create a contact — id 14
  ✔ sees their own contact in their list
  ✔ the row is stamped with A's own user_id by the database

User B
  ✔ starts with an empty list — got 0
  ✔ cannot see A's contact when listing
  ✔ cannot edit A's contact — HTTP 404
  ✔ cannot re-parent A's contact to themselves — HTTP 404
  ✔ cannot delete A's contact — HTTP 404

Signed out
  ✔ listing contacts is rejected — HTTP 401
  ✔ deleting a contact is rejected — HTTP 401

User A, afterwards
  ✔ still has the contact
  ✔ the name was not modified by User B — Ada Lovelace

Server-side validation (User A)
  ✔ rejects a blank name with a clear message — Name is required.
  ✔ rejects an invalid priority with a clear message — Priority must be one of: high, medium, low.

✔ All privacy and validation checks passed.
```

---

## Deployment

```bash
vercel login
vercel link --yes
```

**1. Set the production environment variables.**

```bash
vercel env add NEON_AUTH_COOKIE_SECRET production
vercel env add NEXT_PUBLIC_NEON_AUTH_URL production --no-sensitive
vercel env add NEXT_PUBLIC_NEON_DATA_API_URL production --no-sensitive
```

`--no-sensitive` is required on the two public variables: Vercel defaults new variables to secret visibility, and rejects that for anything carrying a framework public prefix. Do **not** add `DATABASE_URL` — the running app never reads it.

**2. Deploy.**

```bash
vercel --prod
```

**3. Add the deployed domain to Neon Auth's trusted domains.** Without this, sign-up and sign-in fail in production with `403 {"code":"INVALID_ORIGIN"}`, even though they work locally:

```bash
neon neon-auth domain add https://your-app.vercel.app
```

Add every alias you intend to use — Vercel assigns more than one.

**4. Verify against the live URL.**

```bash
npm run test:privacy -- https://your-app.vercel.app
npm run screenshots  -- https://your-app.vercel.app
```

Then open the site in a private window and work through the Definition of Done below.

### Definition of done

All verified against the deployed application at <https://secure-networking-tracker-phi.vercel.app>.

- [x] Live at a public URL
- [x] Sign in and sign out both work
- [x] Add, view, edit, delete, sort and filter all work
- [x] Data survives a refresh
- [x] User A cannot see or change User B's contacts
- [x] Invalid data fails safely with a clear message
- [x] `npm test` passes — 28 tests
- [x] No secret appears in frontend code or Git history

---

## Grading evidence

| Required evidence | Where |
|---|---|
| Automated test output, at least one passing validation test | [Testing](#testing) — 28 passing tests |
| Sign-in and sign-out | [Screenshots](#screenshots) |
| Create, edit, delete, refresh | [Screenshots](#screenshots) |
| Two-account isolation | [Screenshot](#two-accounts-side-by-side) and [scripted check](#two-account-privacy-check) |
| Invalid input failing safely | [Screenshots](#screenshots) |
| Schema and RLS ownership rule | [Database schema](#database-schema), [Authentication and ownership](#authentication-and-ownership) |
| No committed secrets | `.env.example` holds placeholders only; `.gitignore` excludes `.env*` except `.env.example`, and `.neon`. `DATABASE_URL` and the cookie secret appear nowhere in the repository. See [Secret hygiene](#secret-hygiene) for the bundle scan. |

---

## Secret hygiene

`.env.local` (real values) and `.neon` (the CLI's project link) are gitignored; only `.env.example`, with placeholders, is committed.

The claim that no secret reaches the browser is checked against the actual production build rather than assumed:

```bash
npm run build
grep -rl "$DB_PASSWORD"        .next/static/   # no matches
grep -rl "$NEON_AUTH_COOKIE_SECRET" .next/static/   # no matches
grep -rl "DATABASE_URL"        .next/static/   # no matches
```

All three come back empty. So does a search for the Data API host — because the browser only ever calls same-origin `/api/*` routes, even the public Neon endpoints never reach the client bundle. The `NEXT_PUBLIC_*` variables are still declared as public, since they are HTTPS endpoints protected by RLS rather than secrets, and a future client-side call would be safe to make with them.

---

## Known limitations and what I would do next

- **No pagination.** The list loads every matching row. Fine for a personal network; at a few thousand contacts it would need keyset pagination on `(user_id, created_at, id)`.
- **Search is `ILIKE`-based.** Wildcards are escaped and it is pushed down to Postgres, but it is a substring match with no ranking or typo tolerance. A `tsvector` column with a GIN index would be the next step.
- **Deleting is a hard delete** behind a browser `confirm()`. A soft-delete column plus an undo toast would be friendlier and recoverable.
- **No email verification or password reset.** Neon Auth supports both; they are out of scope here, so a forgotten password currently means a new account.
- **Automated tests cover validation, not the UI.** The privacy script covers the API end to end, but there are no component or browser tests — Playwright over the sign-in → add → edit → delete path would close that gap.
- **No follow-up reminders.** The obvious next feature for a networking tracker is "last contacted" plus a nudge when a high-priority contact goes cold.
- **Neon's SDKs are pre-1.0** (`@neondatabase/neon-js` 0.7.0-beta, `@neondatabase/auth` 0.5.0-beta). They are pinned in `package-lock.json`; a minor bump could still be a breaking change.
