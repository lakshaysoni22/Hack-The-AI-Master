"""
TechCorp Employee Management Portal
------------------------------------
A deliberately vulnerable Flask application for the
"The Missing Access Control" cybersecurity training lab.

INTENDED VULNERABILITY (for instructors — do not spoil for learners):
Authentication is implemented correctly using Flask's signed server-side
session. However, the authorization check for sensitive pages (/team and
/admin) does NOT re-check the authenticated user's role from the database
or the signed session. Instead it trusts a separate, plain (unsigned)
cookie named "role" that was set on login for "convenience/UI purposes".

Because that cookie is plain text and not cryptographically protected,
a learner can intercept the request in Burp Suite / edit it in browser
DevTools and change:

    role=employee   ->   role=administrator

...and the server will grant access to a page it should have denied.
This models a very common real-world bug class: trusting client-supplied
authorization data instead of re-validating privileges server-side.

This app is intentionally isolated, non-destructive, and only exploitable
against itself on localhost.
"""

import os
import sqlite3
import logging
import re
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, request, redirect, url_for, render_template,
    session, g, make_response, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "techcorp.db")

app = Flask(__name__)
app.secret_key = os.environ.get("LAB_SECRET_KEY", "techcorp-lab-dev-secret-key-change-me")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ----------------------------------------------------------------------
# Logging (for learner + instructor visibility of what's happening)
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("techcorp-lab")


@app.before_request
def log_request():
    safe_cookies = {k: ("[REDACTED]" if k == "session" else v) for k, v in request.cookies.items()}
    log.info(f"{request.method} {request.path} | cookies={safe_cookies}")


# ----------------------------------------------------------------------
# Database helpers
# ----------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS mission_progress;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL
        );

        CREATE TABLE mission_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_owner TEXT NOT NULL,
            current_mission INTEGER NOT NULL DEFAULT 1,
            flag_captured INTEGER NOT NULL DEFAULT 0,
            knowledge_check_passed INTEGER NOT NULL DEFAULT 0
        );
        """
    )

    users = [
        ("alex", "Alex@123", "Alex Turner", "employee", "IT Support"),
        ("sarah", "Sarah@123", "Sarah Nguyen", "manager", "Security Team"),
        ("admin", "Admin@123", "System Administrator", "administrator", "IT Administration"),
    ]
    for username, pw, display_name, role, dept in users:
        cur.execute(
            "INSERT INTO users (username, password_hash, display_name, role, department) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, generate_password_hash(pw), display_name, role, dept),
        )

    conn.commit()
    conn.close()
    log.info("Database initialized with fresh lab data.")


# ----------------------------------------------------------------------
# Auth helpers
# ----------------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def get_current_user():
    """The AUTHENTICATED user, looked up from the trusted server-side session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


# --- VULNERABLE AUTHORIZATION CHECK -----------------------------------
# This function is intentionally flawed. It decides access based on a
# plain client-side cookie instead of the authenticated user's real role.
def client_supplied_role():
    """
    VULNERABLE BY DESIGN.
    Returns the role from a plain (unsigned) cookie set at login time,
    rather than re-validating against the database / secure session.
    """
    return request.cookies.get("role", "employee")


def role_allows(role, page):
    matrix = {
        "employee": {"dashboard", "profile"},
        "manager": {"dashboard", "profile", "team"},
        "administrator": {"dashboard", "profile", "team", "admin"},
    }
    return page in matrix.get(role, set())


# ----------------------------------------------------------------------
# Mission / progress helpers (simple, session-based for MVP)
# ----------------------------------------------------------------------
def get_progress():
    if "mission" not in session:
        session["mission"] = 1
    if "flag_captured" not in session:
        session["flag_captured"] = False
    return session["mission"], session["flag_captured"]


def set_mission(n):
    session["mission"] = max(int(session.get("mission", 1)), n)


def lab_elapsed_seconds():
    """Return server-tracked elapsed lab time. The browser never controls this clock."""
    started = session.get("lab_started_at")
    if not started:
        return 0
    try:
        start = datetime.fromisoformat(started)
        end = session.get("lab_completed_at")
        if end:
            finish = datetime.fromisoformat(end)
        else:
            finish = datetime.now(timezone.utc)
        return max(0, int((finish - start).total_seconds()))
    except (TypeError, ValueError):
        return 0


def start_lab_session():
    if not session.get("lab_started_at") or session.get("lab_completed_at"):
        session["lab_started_at"] = datetime.now(timezone.utc).isoformat()
        session.pop("lab_completed_at", None)
        session["lab_status"] = "running"


def complete_lab_session():
    if session.get("lab_started_at") and not session.get("lab_completed_at"):
        session["lab_completed_at"] = datetime.now(timezone.utc).isoformat()
    session["lab_status"] = "completed"


# ----------------------------------------------------------------------
# Route: Lab shell (TryHackMe-style split view)
# ----------------------------------------------------------------------
THE_FLAG = "TC{broken_access_control}"


@app.route("/")
def index():
    """Renders the single-page lab shell: task/questions panel on the left,
    a simulated desktop environment (with an embedded browser) on the right."""
    return render_template("lab.html")


@app.route("/api/state")
def api_state():
    """Lightweight state the front-end uses to reflect progress in the task panel."""
    user = get_current_user()
    return jsonify({
        "logged_in": bool(user),
        "username": user["username"] if user else None,
        "role": user["role"] if user else None,
        "lab_status": session.get("lab_status", "not_started"),
        "mission": int(session.get("mission", 1)),
        "flag_captured": bool(session.get("flag_captured", False)),
        "knowledge_check_passed": bool(session.get("knowledge_check_passed", False)),
        "elapsed_seconds": lab_elapsed_seconds(),
    })


@app.route("/api/start-lab", methods=["POST"])
def api_start_lab():
    start_lab_session()
    return jsonify({"status": "running", "elapsed_seconds": lab_elapsed_seconds()})


@app.route("/api/submit-flag", methods=["POST"])
def api_submit_flag():
    data = request.get_json(silent=True) or {}
    submitted = str(data.get("flag") or "").strip()

    # The learner must first demonstrate the vulnerability.  Once that has
    # happened, the flag is validated server-side with an exact comparison.
    exploited = bool(session.get("flag_captured", False))
    correct = exploited and submitted == THE_FLAG

    if correct:
        # Keep the completion state durable even if the learner submits again
        # or refreshes the page.
        session["flag_captured"] = True
        set_mission(4)

    return jsonify({
        "correct": correct,
        "exploited": exploited,
        "message": (
            "Correct flag."
            if correct
            else (
                "Reach the Admin Panel through the authorization flaw first."
                if not exploited
                else "Incorrect flag."
            )
        ),
    })


@app.route("/api/knowledge-check", methods=["POST"])
def api_knowledge_check():
    data = request.get_json(silent=True) or {}
    auth_answer = (data.get("auth_answer") or "").lower()
    authz_answer = (data.get("authz_answer") or "").lower()
    summary = (data.get("summary") or "").strip()

    # Validate the concepts, not a single exact sentence.  This accepts
    # natural answers while avoiding accidental substring matches.
    auth_patterns = [
        r"\bidentity\b", r"\bwho\s+(?:you|the user)\s+are\b",
        r"\bverify\w*\s+(?:the\s+)?(?:user'?s?\s+)?identity\b",
        r"\bidentify\w*\s+(?:the\s+)?user\b",
    ]
    authz_patterns = [
        r"\bpermission\w*\b", r"\baccess\b", r"\bauthori[sz]\w*\b",
        r"\ballow\w*\b", r"\b(right|rights)\b", r"\bresource\w*\b",
    ]

    auth_ok = any(re.search(p, auth_answer) for p in auth_patterns)
    authz_ok = any(re.search(p, authz_answer) for p in authz_patterns)
    summary_words = re.findall(r"\b\w+\b", summary)
    summary_ok = len(summary_words) >= 8

    passed = auth_ok and authz_ok and summary_ok and bool(session.get("flag_captured", False))
    session["knowledge_check_passed"] = passed
    if passed:
        set_mission(5)
        complete_lab_session()
    return jsonify({
        "passed": passed,
        "auth_ok": auth_ok,
        "authz_ok": authz_ok,
        "summary_ok": summary_ok,
        "flag_captured": bool(session.get("flag_captured", False)),
    })


# ----------------------------------------------------------------------
# Routes: Authentication
# ----------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            # Preserve the lab session while replacing only the authentication
            # identity.  session.clear() here used to erase the timer, mission
            # progress and flag state, which made the UI appear to lose ticks.
            lab_state = {
                key: session.get(key)
                for key in (
                    "lab_started_at",
                    "lab_completed_at",
                    "lab_status",
                    "mission",
                    "flag_captured",
                    "knowledge_check_passed",
                )
                if key in session
            }

            # --- Authentication still uses the secure, signed session. ---
            session.clear()
            session.update(lab_state)
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            if session.get("lab_status") == "running":
                set_mission(2)

            resp = make_response(redirect(url_for("dashboard")))
            # --- Flawed part: a plain, client-readable/writable cookie is also
            # set, and it is this cookie (not the DB role) that authorization
            # checks below will trust. ---
            resp.set_cookie("role", user["role"], httponly=False, samesite="Lax")
            log.info(f"Login success: {username} (role={user['role']})")
            return resp
        else:
            error = "Invalid username or password."
            log.info(f"Login failed for username='{username}'")

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("role")
    return resp


# ----------------------------------------------------------------------
# Routes: Portal pages
# ----------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    user = get_current_user()
    if session.get("lab_status") == "running" and user:
        set_mission(3)
    return render_template("dashboard.html", user=user, page_role=client_supplied_role())


@app.route("/profile")
@login_required
def profile():
    user = get_current_user()
    return render_template("profile.html", user=user, page_role=client_supplied_role())


@app.route("/team")
@login_required
def team():
    user = get_current_user()
    role = client_supplied_role()  # <-- vulnerable check
    if not role_allows(role, "team"):
        return render_template("denied.html", user=user, attempted="Team Management"), 403

    db = get_db()
    team_members = db.execute(
        "SELECT display_name, role, department FROM users ORDER BY role"
    ).fetchall()
    return render_template("team.html", user=user, team_members=team_members, page_role=role)


@app.route("/admin")
@login_required
def admin():
    user = get_current_user()
    role = client_supplied_role()  # <-- vulnerable check
    if not role_allows(role, "admin"):
        return render_template("denied.html", user=user, attempted="Admin Panel"), 403

    # Successful exploitation path
    flag_awarded = False
    if role != user["role"]:
        # The authenticated user's real DB role differs from the role that
        # granted access -> this proves the authorization bypass occurred.
        if session.get("lab_status") == "running":
            session["flag_captured"] = True
            set_mission(4)
        flag_awarded = True
        log.info(
            f"VULNERABILITY TRIGGERED: user '{user['username']}' (real role="
            f"{user['role']}) accessed /admin using spoofed role cookie='{role}'"
        )

    return render_template(
        "admin.html",
        user=user,
        page_role=role,
        flag_awarded=flag_awarded,
        flag_previously_captured=session.get("flag_captured", False),
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Internal server error."), 500


# ----------------------------------------------------------------------
# Lab reset endpoint (safe: only touches this app's own SQLite DB + session)
# ----------------------------------------------------------------------
@app.route("/lab/reset", methods=["POST"])
def lab_reset():
    init_db()
    session.clear()
    resp = make_response(jsonify({"status": "ok"}))
    resp.delete_cookie("role")
    return resp


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
