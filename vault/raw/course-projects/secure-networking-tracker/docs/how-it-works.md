# How this app works

Notes for explaining the system without help: the schema, the ownership rule, and what happens on a single request. Read top to bottom once; the last section is the awkward questions.

---

## 1. The one-paragraph version

A signed-in user gets a private list of contacts. The browser never talks to the database. It calls our own `/api/*` routes; those routes check the session cookie, validate the request body, mint a short-lived JWT for that user from Neon Auth, and call the Neon Data API with it. Postgres reads the user's id out of that JWT and applies Row Level Security, so a query for "all contacts" physically cannot return another user's rows. Ownership is decided by the database, not by our code.

---

## 2. The schema

One table, `public.contacts`:

| Column | Type | Why it looks like this |
|---|---|---|
| `id` | `bigint` identity, PK | Surrogate key. Nothing about the person. |
| `user_id` | `text NOT NULL DEFAULT auth.user_id()` | The owner. **This is the whole security model.** |
| `name` | `text NOT NULL` | The only required field. Two CHECK constraints: not blank after trimming, ≤ 120 chars. |
| `company`, `role`, `where_met`, `notes` | `text` nullable | Optional. Blank input is stored as `NULL`, never `''`, so "absent" has one representation. |
| `priority` | `contact_priority NOT NULL DEFAULT 'medium'` | A Postgres **enum** of `high, medium, low`. |
| `created_at`, `updated_at` | `timestamptz NOT NULL DEFAULT now()` | `updated_at` is maintained by a trigger, not by the client. |

Three details worth being able to defend:

**`user_id` is `text`, not `uuid`.** `auth.user_id()` returns the JWT's `sub` claim as `text`. Making the column `text` means the default, the policies, and the column all compare the same type with no casting.

**`priority` is an enum, not a `text` + CHECK.** An invalid value is rejected by the type system itself, and it makes sorting meaningful: Postgres orders enums by *declaration* order, so `ORDER BY priority ASC` gives high → medium → low, which is the order a person actually wants. A `text` column would sort alphabetically: high, low, medium.

**Index is `(user_id, created_at DESC)`.** Every query this app runs is "my contacts, newest first". Leading with `user_id` lets one index serve the filter and the sort together.

---

## 3. The ownership rule

> **A row belongs to whoever's JWT created it, and only that user can read or change it.**

Enforced three times, at three different layers. Only the middle one is load-bearing.

### Layer 1 — the database assigns ownership

```sql
user_id text NOT NULL DEFAULT (auth.user_id())
```

The API never sends `user_id`. The Zod schema doesn't even have that field, so if a client posts one it is dropped before the insert. The value can only come from the verified token. There is no code path that lets a caller choose an owner.

### Layer 2 — Row Level Security filters every statement

```sql
ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contacts FORCE  ROW LEVEL SECURITY;
```

`ENABLE` turns policies on. `FORCE` also applies them to the table's *owner* — without it, `neondb_owner` would bypass every policy.

Four policies, one per operation, all for the `authenticated` role:

```sql
CREATE POLICY contacts_select_own ON public.contacts
  FOR SELECT TO authenticated
  USING ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_insert_own ON public.contacts
  FOR INSERT TO authenticated
  WITH CHECK ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_update_own ON public.contacts
  FOR UPDATE TO authenticated
  USING      ((SELECT auth.user_id()) = user_id)
  WITH CHECK ((SELECT auth.user_id()) = user_id);

CREATE POLICY contacts_delete_own ON public.contacts
  FOR DELETE TO authenticated
  USING ((SELECT auth.user_id()) = user_id);
```

**`USING` vs `WITH CHECK` — the distinction to have ready:**

- `USING` filters rows that already exist. It answers *"which rows may this statement see or touch?"* It is silently added to `SELECT`, `UPDATE` and `DELETE` as an extra `WHERE` clause.
- `WITH CHECK` inspects the row *as it will be after the write*. It answers *"is this row allowed to exist looking like that?"* It applies to `INSERT` and `UPDATE`.

**Why `UPDATE` needs both.** With only `USING`, a user could target a row they legitimately own and change `user_id` to someone else's id. `USING` was satisfied — they did own it at the start. Nothing would check the result, so the row would silently move into another person's list. That is both a data-loss bug and a way to plant rows in someone else's account. `WITH CHECK` re-evaluates the rule against the *new* row and rejects it.

There is also a `BEFORE UPDATE` trigger that resets `NEW.user_id = OLD.user_id`, so ownership is pinned even if a policy were later loosened.

**`anonymous` is granted nothing** on this table, so an unauthenticated caller has no privileges to exercise in the first place.

### Layer 3 — the application checks too

Route handlers return `401` before touching the database, and `/contacts` redirects signed-out visitors. This is convenience and defence in depth. **It is not what makes the data private.** If you deleted every line of it, RLS would still hold.

---

## 4. What happens on one request

Editing contact 42:

```
1. Browser            PATCH /api/contacts/42  {"priority":"low"}
                      Same origin. No token, no database URL in the bundle.

2. Route handler      auth.getSession() reads the httpOnly session cookie.
                      No session → 401, stop.

3. Validation         Zod parses the body. Unknown fields (including user_id)
                      are dropped; an invalid priority returns 400 with a
                      per-field message. Nothing reaches the database yet.

4. Token              The server asks Neon Auth for a short-lived JWT for
                      this user. This happens server-side; the browser never
                      sees a token.

5. Data API           PATCH .../contacts?id=eq.42 with Authorization: Bearer <jwt>.
                      PostgREST verifies the JWT against Neon's JWKS and
                      switches the Postgres role to `authenticated`.

6. Postgres           auth.user_id() now returns this user's sub claim.
                      contacts_update_own applies:
                        USING      → is row 42 mine?      (else it isn't visible)
                        WITH CHECK → is the result mine?  (else reject)
                      Trigger refreshes updated_at and pins user_id.

7. Response           Rows updated: 1 → 200 with the row.
                      Rows updated: 0 → the handler returns 404.
```

**Why 404 and not 403.** Under RLS, a row you don't own is not "forbidden" — it is *invisible*. The `UPDATE` matches zero rows, exactly as if the id didn't exist. Returning 403 would leak that id 42 exists and belongs to someone; 404 says nothing. The handler doesn't need an ownership check to produce this — it falls out of the database returning no rows.

---

## 5. Validation happens three times, on purpose

| Where | What it catches | Trusted? |
|---|---|---|
| The browser form | Typos, immediate feedback | **No.** Anyone can `curl` the API. |
| `src/lib/validation/contact.ts` (Zod, in the route handler) | Every write, whatever the client | **Yes** — this is the real check, and the one the 28 tests cover. |
| Postgres CHECK constraints + the enum | Anything that reaches the DB by any route | **Yes** — the last line. |

The dialog uses `noValidate`, which is deliberate: the browser's own popup is suppressed so the message on screen is the one the *server* sent back. What you see is the trusted validation, not a client-side imitation of it.

---

## 6. Secrets: what is public and why that's fine

| Value | Public? | Reasoning |
|---|---|---|
| `NEXT_PUBLIC_NEON_AUTH_URL` | Yes | An HTTPS endpoint. Useless without credentials. |
| `NEXT_PUBLIC_NEON_DATA_API_URL` | Yes | Same. Hitting it without a JWT returns `missing authentication credentials`; hitting it *with* one returns only that user's rows, because RLS. |
| `NEON_AUTH_COOKIE_SECRET` | **No** | Signs the session cookie. Leaking it means forging sessions. |
| `DATABASE_URL` | **No** | Direct Postgres access as the owner. Used only to apply `db/schema.sql` from a developer machine; the running app never reads it. |

The `NEXT_PUBLIC_` endpoints are safe to expose *because* RLS is doing the work. That is the point of the design: the security does not depend on hiding a URL.

In this build the browser doesn't even receive those URLs, since every call goes through `/api/*`. They stay declared as public because they are safe to be, and a future client-side call would need no change.

---

## 7. Questions you should have an answer for

**"Why route through your own API when the Data API is designed for direct browser access?"**
Both are safe — RLS protects the rows either way. Going through the backend adds a second independent layer: trusted validation before anything reaches the database, normalised error messages so raw Postgres text never reaches the client, and control over query shape. RLS is still the boundary; the API layer is depth, not a substitute.

**"What if there's a bug in your API layer?"**
Then RLS still holds. The worst a handler bug can do is return the wrong subset of *your own* rows. It cannot reach another user's data, because the database is applying the filter using an identity the handler cannot forge.

**"Could a user forge `user_id`?"**
Three things stop it independently: the field isn't in the Zod schema so it is dropped from the payload; `WITH CHECK` rejects any row whose `user_id` isn't the caller's; and the trigger pins `user_id` on update. Forging the id would require forging the JWT, which requires the signing key.

**"Why is `FORCE ROW LEVEL SECURITY` there?"**
Without it, the table owner (`neondb_owner`) bypasses every policy. The app connects as `authenticated`, so it isn't strictly required — but it means a future script that connects as the owner doesn't silently sidestep the entire security model.

**"What does `auth.user_id()` actually do?"**
It comes from the `pg_session_jwt` extension, which the Neon Data API installs. PostgREST verifies the incoming JWT against Neon Auth's JWKS and puts its claims into the session; `auth.user_id()` returns the `sub` claim as text. If the token is missing or invalid, the request never reaches a policy.

**"How do you know the two-user isolation actually works?"**
`npm run test:privacy` proves it against the deployed app: it signs up two accounts over real HTTP, has A create a contact, then has B attempt to list, read, edit, re-parent and delete it. Every attempt returns 404, and a signed-out client gets 401.

**"Where would this break first at scale?"**
The list endpoint has no pagination — it returns every matching row. Fine for a personal network, wrong at a few thousand contacts; the fix is keyset pagination on `(user_id, created_at, id)`, which the existing index already supports.
