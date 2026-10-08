# PROJECT_MANUAL_LAB_ANALYSIS

## Current Architecture

The HACK THE AI CTF Platform is currently built with:
- **Backend:** Flask, Python
- **Database:** SQLite (using `database/schema.sql` and `hacktheai.db`)
- **Frontend:** HTML, Vanilla CSS (in `static/css`), JavaScript
- **Data Initialization:** `seed_db.py`

### Existing Routes (`app.py` & Blueprints)
- `/`: Landing page
- `/login`, `/register`, `/logout`: Authentication
- `/dashboard`: User dashboard
- `/labs`: List of all Guided Labs
- `/lab/<lab_id>`: Guided Lab details
- `/lab/<lab_id>/workstation`: Guided Lab workstation
- API endpoints: `/api/quiz`, `/api/hint`, `/api/evidence`, `/api/flag`
- `/admin`, `/leaderboard`: Blueprints for admin and leaderboard views

### Database Schema
- **Users:** `users`
- **Guided Labs:** `labs`, `missions`, `mission_progress`, `lab_progress`
- **Evaluation:** `evidence`, `evidence_progress`, `flags`, `mission_quiz`, `quiz_attempts`
- **Hints:** `hints`, `hint_usage`
- **Other:** `achievements`, `audit_logs`

### Current Models & Progress
- **Authentication:** Uses Werkzeug `generate_password_hash` & `check_password_hash`. Session-based (`session['user_id']`).
- **XP / Progress Implementation:** User progress is tracked through `lab_progress`, `mission_progress`, and `evidence_progress`. The `lab_progress` tracks overall score and completion percentage. Evaluated by central services (`services/progress_service.py`, `quiz_service.py`).
- **Guided Labs:** Linear flow (Story -> Mission -> Guidance -> Evidence -> Quiz -> Flag -> XP).

### Existing UI & Navigation
- The navigation (in `base.html` or similar) likely includes Dashboard, Labs, Challenges, etc. Some of these (`/challenges`, `/docs`, `/pricing`) are currently stubs (`stub.html`).
- The `workstation.html` is the current interface for guided lab interaction.

## Gap Analysis for Manual Labs System

The current system only supports "Guided Labs" with predefined linear missions. To support the "Manual Labs" requirement:
1. **Database Additions:** We need new tables (e.g., `manual_labs`, `manual_lab_progress`, `manual_lab_objectives`) to distinguish from guided labs.
2. **Routes & Views:** 
   - `/manual-labs`: Discovery page with filters.
   - `/manual-lab/<id>`: Details and objective view.
   - `/manual-lab/<id>/environment`: The interface to start/manage the isolated target and capture the flag.
3. **Backend Logic:** Ability to handle "Start Environment" (even if mocked initially) and submit flags specifically for manual labs.
4. **Navigation:** Needs an update in `base.html` to clearly show the unified navigation items (Dashboard, Labs, Manual Labs, Challenges, Leaderboard, Achievements, Learning, Profile).
