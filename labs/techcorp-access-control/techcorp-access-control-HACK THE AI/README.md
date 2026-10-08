# The Missing Access Control
### TechCorp Employee Management Portal — Cybersecurity Training Lab

## Lab Purpose

This is a beginner-friendly, self-contained cybersecurity training lab that teaches the
difference between **authentication** and **authorization**, and how broken access control
vulnerabilities happen in real web applications.

You'll play as **Alex Turner**, a Junior Cybersecurity Analyst at TechCorp, investigating whether
employees can improperly access resources meant for higher-privileged roles inside an internal
Employee Management Portal.

This lab is intentionally vulnerable **only within this project**. It is designed to run entirely
on your local machine (e.g., Kali Linux) with no external dependencies.

## Learning Objectives

By completing this lab, you will practice and understand:

- Authentication vs. Authorization
- Role-Based Access Control (RBAC)
- How access-control decisions are enforced (or fail to be enforced) server-side
- Reading and interpreting HTTP requests and responses
- Cookies and sessions
- Using browser Developer Tools
- Using Burp Suite to intercept and modify requests
- Identifying an authorization weakness
- Writing up a basic security finding

**Authentication** = Who are you?
**Authorization** = What are you allowed to access or do?

## Requirements

- A Linux machine (tested on Kali Linux)
- Python 3.9+
- Firefox (or any browser)
- Burp Suite Community Edition (or just browser DevTools if you prefer)
- No internet access required

## Installation

```bash
git clone <this-project-folder>  # or copy the folder to your machine
cd techcorp-access-control
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Or simply run:

```bash
chmod +x start.sh
./start.sh
```

The application will be available at: **http://127.0.0.1:5000**

Opening that URL loads a TryHackMe-style split view:
- **Left panel** — the story, missions, hints, flag submission, and knowledge check.
- **Right panel** — a simulated desktop environment. Double-click the **Firefox** icon (or use
  "Open Browser" in the left panel) to launch the actual vulnerable portal inside a browser-style
  window. A **Terminal** icon is also available for note-taking (it does not execute real
  commands — use your own terminal/Burp Suite for real traffic interception).

## Starting the Lab

1. Run `./start.sh` (or the manual steps above).
2. Open Firefox and navigate to `http://127.0.0.1:5000`.
3. (Optional) Configure Burp Suite as your browser's proxy if you want to intercept traffic from
   the start.
4. Follow the on-screen story and missions — the lab will guide you step by step.

## Resetting the Lab

If you want to start over from a clean state at any time:

```bash
./reset.sh
```

This deletes and recreates the lab's local SQLite database only. It does not touch anything
outside this project folder.

You can also reset from within the app on the final "Lab Complete" screen.

## How the Storyline Works

The lab is structured as a 5-mission investigation:

1. **Identify Your Identity** — Log in and confirm authentication.
2. **Map the Portal** — Explore the portal and its pages.
3. **Follow the Evidence** — Use Burp Suite or DevTools to inspect real HTTP traffic.
4. **The Broken Door** — Attempt to reach a restricted resource and capture the flag.
5. **Explain the Incident** — Reflect on what happened.

A final **Knowledge Check** asks you to explain authentication vs. authorization in your own
words before the lab is marked complete.

You will only be given an **Employee** account. Discovering the vulnerability is part of the
exercise — no exploit steps are spelled out for you directly, but progressive hints are available
in Mission 3 if you get stuck.

## How to Test the Lab

A good end-to-end test run looks like:

1. Start the app and open it in Firefox.
2. Log in with the Employee credentials shown in Mission 1.
3. Browse Dashboard and My Profile (should work normally).
4. Try Team Management and Admin Panel from the nav (should be denied).
5. Open Burp Suite / DevTools and inspect the requests/cookies involved.
6. Use what you observe to reach the Admin Panel anyway.
7. Confirm you receive the flag.
8. Complete Mission 5 and the Knowledge Check.
9. Try `./reset.sh` and confirm the lab returns to its original state.

## Notes

- This application deliberately contains a security flaw for educational purposes. Do not deploy
  it outside of an isolated local training environment.
- The vulnerability, exploitation path, and flag are documented separately for
  instructors in `INSTRUCTOR.md` — that file is not meant to be read before attempting the lab.
