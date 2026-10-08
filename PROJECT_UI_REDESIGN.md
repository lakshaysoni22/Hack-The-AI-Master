# PROJECT_UI_REDESIGN

## 1. Existing UI
The current UI is functional but basic. It uses simple HTML templates (e.g., `base.html`, `dashboard.html`, `workstation.html`, `labs.html`, `login.html`, `register.html`, `landing.html`).
It lacks a modern, unified design language, relies heavily on basic structural CSS without a consistent variable-driven theme, and doesn't offer the visual immersion expected of a cybersecurity training platform.

## 2. Existing Routes
The Flask backend provides the following main routes:
- `/` - Landing page
- `/login`, `/register`, `/logout` - Authentication
- `/dashboard` - User dashboard (overall stats, recent labs)
- `/labs` - Lab discovery
- `/lab/<lab_id>` - Lab details
- `/lab/<lab_id>/workstation` - The core interactive lab environment
- `/challenges`, `/docs`, `/pricing` - Stub pages
- API routes: `/api/quiz`, `/api/hint`, `/api/evidence`, `/api/flag` (All POST, returning JSON)
- Admin and leaderboard blueprints

## 3. Existing Components
- Simple navigation bars (not structured as a modern app shell).
- Basic lists for labs and missions.
- A functional but visually uninspiring workstation with basic HTML forms for flags/quizzes.
- Basic alerts for error/success messages.

## 4. Problems Found
- No cohesive design system (CSS variables).
- Lack of modern cybersecurity aesthetics (dark mode, glowing accents, elevated surfaces).
- The workstation layout doesn't feel like a professional cyber range.
- The UI doesn't visually communicate the excitement and gamification of learning cybersecurity.
- CSS is likely monolithic or unstructured given the few files found.
- Lack of micro-interactions and smooth transitions.

## 5. Redesign Architecture
- **Theme**: Dark mode by default, elevated panels, cybersecurity green primary accent (`--accent`, `--success`), dark backgrounds (`--bg-primary`, `--bg-secondary`, `--bg-card`).
- **Layout Shell**: Desktop sidebar + top nav. Mobile drawer + top nav.
- **Workstation**: Tabbed interface or multi-panel layout (Browser, Terminal, Evidence, Instructions).
- **CSS Architecture**: Split into logical files (variables, reset, typography, components, layout, pages).
- **JavaScript**: Enhance interactivity (tabs, modals, toasts, progress animations) without breaking the simple Flask routing and API calls.

## 6. Files That Will Be Changed
- All HTML templates in `templates/` (`base.html`, `dashboard.html`, `labs.html`, `lab_detail.html`, `workstation.html`, `landing.html`, `login.html`, `register.html`, etc.)
- Existing CSS in `static/css/` will be completely overhauled and modularized.
- Existing JS in `static/js/` (if any) will be updated to match the new UI interactions.

## 7. Files That Must Remain Compatible
- Backend python files: `app.py`, `routes/*`, `services/*`, `seed_db.py`.
- Database schemas: `database/schema.sql`.
- The APIs must continue to receive JSON and return JSON exactly as they do now.
- Jinja template variables (e.g., `{{ user_id }}`, `{{ labs }}`, `{{ missions }}`) must still be consumed properly.
