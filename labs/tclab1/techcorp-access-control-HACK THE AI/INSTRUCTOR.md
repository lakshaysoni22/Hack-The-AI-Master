# INSTRUCTOR GUIDE (Do not distribute to learners)

## Intended Vulnerability

**Class:** Broken Access Control — trusting client-controlled authorization data
(CWE-639 / OWASP A01:2021 – Broken Access Control).

**Mechanism:**

- Authentication is implemented correctly: `POST /login` checks credentials against
  `werkzeug.security.check_password_hash`, and on success sets a secure, cryptographically
  signed Flask session cookie (`session['user_id']`). This part of the app is **not** vulnerable —
  you cannot forge a valid authenticated session without knowing a real password.
- On successful login, the app **also** sets a second, plain (unsigned, readable/writable)
  cookie: `role=<the user's role>`.
- The route handlers for `/team` and `/admin` (see `app.py`, function `client_supplied_role()`)
  make their authorization decision by reading this `role` cookie directly from the request,
  instead of re-checking `users.role` in the database for the authenticated `session['user_id']`.
- Because the `role` cookie is not signed or otherwise protected, a learner who is authenticated
  as `alex` (real role: `employee`) can intercept a request in Burp Suite (or edit
  `document.cookie` / the Storage panel in Firefox DevTools) and change:

  ```
  Cookie: session=<unchanged, still valid>; role=employee
  ```

  to:

  ```
  Cookie: session=<unchanged, still valid>; role=administrator
  ```

  and resend the request to `GET /admin`. The server will grant access because
  `role_allows("administrator", "admin")` is `True`, even though the authenticated user's real
  database role is still `employee`.

## Expected Exploitation Path

1. Log in as `alex` / `Alex@123`.
2. Browse `/dashboard` and `/profile` (allowed) and `/team`, `/admin` (denied, HTTP 403).
3. In Burp Suite (Proxy > HTTP history, or Repeater) or Firefox DevTools > Storage > Cookies,
   locate the `role` cookie value (`employee`) sent alongside the `session` cookie.
4. Change the `role` cookie value to `administrator` (or `manager` for `/team`).
5. Resend the request to `GET /admin`.
6. The app detects `role != user['role']` server-side (this check exists purely to award the
   flag and log the event — it does not affect the vulnerability itself) and displays:

   ```
   FLAG: TC{broken_access_control}
   ```

   The flag is also echoed on the Mission 4 page once `session['flag_captured']` is set.

## Interface Notes

The lab now presents as a single-page, TryHackMe-style shell (`templates/lab.html` +
`static/lab.js` + `static/lab.css`):

- The left panel holds all mission/task content and a graded flag-submission box
  (`/api/submit-flag`) and knowledge check (`/api/knowledge-check`).
- The right panel is a cosmetic "virtual desktop." Its Firefox icon opens the real vulnerable
  Flask routes (`/login`, `/dashboard`, `/team`, `/admin`, etc.) inside an `<iframe>` styled as a
  browser window — this is the actual attack surface. The Terminal icon is decorative/flavor
  text only; it does not execute real shell commands, since the exploit only requires
  cookie/DevTools/Burp manipulation of real HTTP traffic to `127.0.0.1:5000`.
- `/api/submit-flag` only returns `correct: true` if the current session actually triggered the
  vulnerability (`session['flag_captured']`) **and** the submitted string matches the flag exactly
  — this prevents learners from guessing the flag without exploiting the app.

## Flag

```
TC{broken_access_control}
```

The flag is only rendered inside `templates/admin.html` (and subsequently `mission4.html` /
`complete.html`) after the server detects a role mismatch indicating successful exploitation. It
is not present in any source file, comment, static asset, robots.txt, or the learner README.

## Mission Solutions / Answers

- **Mission 1 question** ("What security process has successfully verified Alex's identity?"):
  Expected answer: *Authentication*.
- **Mission 5 questions:**
  1. Alex was authenticated as the Employee account (`alex`).
  2. The Admin Panel (`/admin`), intended for Administrators only.
  3. Yes — authentication succeeded; the session is valid.
  4. No — the account's real role (`employee`) does not permit Admin Panel access.
  5. Authorization (access control), which should be enforced server-side against a trusted
     source of truth (e.g., the database record tied to the authenticated session).
  6. The server trusted a client-controlled cookie (`role`) instead of re-validating the
     authenticated user's actual role from the database on every sensitive request.

## Knowledge Check Answer Guidance

- **Authentication verifies:** identity / who the user is.
- **Authorization verifies:** permissions / what the user is allowed to access or do.
- **Summary:** Learner should articulate that authentication only confirms *who* someone is; a
  system can still be broken if it fails to independently and server-side verify *what* that
  authenticated identity is permitted to do — e.g., by trusting a client-supplied value such as a
  role cookie or hidden form field instead of checking a trusted, server-controlled source
  (database / signed session) on every request.

The MVP validator (`/knowledge-check` in `app.py`) does simple keyword matching:
- Authentication answer must contain one of: `identity`, `who`, `verif`.
- Authorization answer must contain one of: `permission`, `access`, `allow`, `right`, `action`,
  `resource`.
- Summary must be at least 8 words.

This is intentionally lenient for an MVP; tighten as needed for a real classroom setting.

## Troubleshooting

- **"database/techcorp.db not found" / login fails immediately after clone:** Run
  `python3 -c "from app import init_db; init_db()"` once, or just run `./start.sh`, which does
  this automatically on first run.
- **Cookies not visible in Burp:** Make sure Burp's proxy is configured in Firefox and that
  "Intercept" is off (or you're using HTTP history / Repeater) so normal browsing traffic is
  captured without needing to manually forward every request.
- **`role` cookie not present:** Confirm the learner actually logged in through `/login` — the
  cookie is only set on a successful authentication response. Logging out clears it.
- **Flag doesn't appear after editing the cookie:** Ensure the `session` cookie (the real,
  signed Flask session) is still being sent — the exploit only requires editing `role`, not
  removing or forging the session. If the session is missing, the user gets redirected to
  `/login` instead.
- **Port already in use:** Another process may be bound to 5000. Stop it or change the port in
  the `app.run(...)` call in `app.py`.

## How to Verify the Vulnerability Yourself

```bash
./start.sh
# In another terminal:
curl -s -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:5000/login \
  -d "username=alex&password=Alex@123"

# Inspect cookies.txt — note the 'role' cookie value (employee).
# Manually edit cookies.txt to change role to 'administrator', then:
curl -s -b cookies.txt http://127.0.0.1:5000/admin | grep -i "FLAG"
```

You should see the flag text appear in the `/admin` response only after the `role` cookie has
been changed to `administrator` (or `manager`, for `/team`).

## Reset Verification

Run `./reset.sh`, then confirm:
- `database/techcorp.db` has been recreated with the three default users.
- The flag cannot be obtained by simply visiting `/admin` immediately after a fresh login as
  `alex` without modifying the `role` cookie (should return 403 / denied page).
