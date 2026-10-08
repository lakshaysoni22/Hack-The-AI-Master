# Project Analysis: HACK THE AI CTF Platform

## Current Architecture
- The application is a monolithic Flask application primarily contained in `app.py`.
- It uses a SQLite database (`database/hacktheai.db`) accessed directly via `sqlite3` driver inside route handlers.
- The project skeleton has empty directories for `routes/`, `services/`, and `data/` which are unused.
- Labs 1-5 have empty directory placeholders inside `labs/`.

## Existing Routes
- `/` - Landing page
- `/login` - User login
- `/register` - User registration
- `/logout` - Session termination
- `/dashboard` - User dashboard (has hardcoded UI elements and fake data)
- `/challenges`, `/leaderboard`, `/docs`, `/pricing` - Stub endpoints
- `/labs` - Lab listing
- `/lab/<lab_id>` - Lab details
- `/lab/<lab_id>/workstation` - Lab workstation interface
- `/api/quiz` (POST) - Quiz validation
- `/api/evidence` (POST) - Evidence collection
- `/api/flag` (POST) - Flag validation

## Database Tables
- `users`: id, username, password, created_at
- `labs`: id, name, topic, difficulty, description
- `missions`: id, lab_id, mission_number, title, description
- `mission_progress`: id, user_id, lab_id, mission_id, status, completed_at
- `evidence`: id, lab_id, title, description
- `evidence_progress`: id, user_id, evidence_id, collected
- `quiz_attempts`: id, user_id, mission_id, answer, correct, timestamp
- `lab_progress`: id, user_id, lab_id, score, percentage, status, completed_at
- `flags`: id, lab_id, flag_value
- `achievements`: id, title, description
- `audit_logs`: id, user_id, action, details, timestamp

## Relationships
- Foreign keys properly map users to their progress across labs, missions, evidence, and quizzes.
- `missions`, `evidence`, and `flags` belong to `labs`.

## Current Labs
- Lab 1: The Missing Access Control (Authentication vs Authorization)
- Lab 2: The Exposed Employee File (Information Disclosure)
- Lab 3: The Missing Employee Access (IDOR)
- Lab 4: The Tricked Support Ticket (Cross-Site Scripting)
- Lab 5: The Fake Login Trap (Phishing)

## Current Missions & Flags
- Only Lab 4 and Lab 5 missions are populated in the database via `seed_db.py`. Labs 1-3 have no missions or flags defined.
- Lab 4 has flag `TECHCORP{xss_ticket_found}` and Lab 5 has flag `TECHCORP{human_firewall}`. Labs 1-3 have no flags seeded.

## Current Problems (Identified & Verified)
1. Monolithic `app.py` makes maintenance difficult.
2. Labs 1-3 have no real missions or flags in `seed_db.py`.
3. Lab 5 mission progress is not initialized in `/register` or `seed_db.py`.
4. Lab unlocking logic is hardcoded (Lab 1 & 2 Completed, Lab 3 In Progress, etc. in seed_db, or available in register) and not dynamically evaluated based on prerequisites.
5. Workstation and Dashboard XP/evidence values are hardcoded in the templates.
6. Evidence collection `/api/evidence` just adds 25 points unconditionally, allowing infinite XP grinding.
7. Quiz answers are hardcoded directly in `app.py`.
8. Quiz mission eligibility is not properly enforced (can skip missions).
9. Hint system is missing entirely.
10. Leaderboard, achievements, and audit logging are stubs or unimplemented.
11. Flask secret key is hardcoded in `app.py`.
12. Flask debug mode is enabled by default.
13. CSRF protection is missing. Rate limiting is missing.

## Proposed Architecture
- Migrate to a Blueprint-based architecture mapping to the `routes/` directory (auth, dashboard, labs, api, leaderboard, profile, admin).
- Extract database and business logic to the `services/` directory (auth_service, progress_service, quiz_service, etc.).
- Introduce `Flask-WTF` for CSRF and `Flask-Limiter` for rate limiting.
- Containerize isolated vulnerable targets in `labs/lab1` to `labs/lab5` utilizing Docker, interacting with the primary platform securely.
