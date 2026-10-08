"""
Clean integration of the four remaining labs (IDOR, Info Disclosure, Lab4-XSS, Lab5-Phishing)
into the CTF platform's UploadedLab data model.

Rather than relying on the fragile regex-based INSTRUCTOR.md auto-parser (which produces
garbage titles/mission text for these zips, as demonstrated), this script:
  1. Extracts each ZIP into data/uploaded_labs/ using the platform's own safe extraction
     logic (LabZipParser._safe extraction path is reused via parse_zip, but we override the
     resulting manifest fields with accurate, hand-verified content).
  2. Builds an accurate LabManifest (title, category, difficulty, concept, description,
     missions with real objectives/instructions/hints/questions, flags, docker_config,
     target_app_path) based on each lab's INSTRUCTOR.md / app.py ground truth.
  3. Saves it via the same save_manifest_to_db() used by the real upload endpoint, then
     publishes it.

This replaces the four low-quality auto-parsed rows created by integrate_labs.py.
"""
import os, sys, uuid, json

os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('SECRET_KEY', 'dev-integration-script')

from app import app, db
import models
from services.lab_parser_service import LabZipParser, save_manifest_to_db, LabManifest

UPLOAD_DIR = None


def extract_only(parser, zip_path, extract_dir):
    """Reuse the parser's safe-extraction logic without trusting its heuristic metadata."""
    import zipfile
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for member in zf.infolist():
            if member.is_dir():
                continue
            member_path = os.path.normpath(member.filename)
            if member_path.startswith('..') or os.path.isabs(member_path):
                continue
            zf.extract(member, extract_dir)
    root = parser._find_lab_root(extract_dir)
    return extract_dir, root


def build_manifest(title, category, difficulty, concept, description, estimated_time,
                    missions, flags, target_app_path, ports=(5000,)):
    m = LabManifest()
    m.lab_id = f"ulab-{uuid.uuid4().hex[:8]}"
    m.title = title
    m.category = category
    m.difficulty = difficulty
    m.concept = concept
    m.description = description
    m.estimated_time = estimated_time
    m.storyline = ''
    m.missions = missions
    m.flags = flags
    m.docker_config = {
        "has_dockerfile": True,
        "has_compose": True,
        "dockerfile_path": "Dockerfile",
        "compose_path": "docker-compose.yml",
        "ports": list(ports),
    }
    m.target_app_path = target_app_path
    m.total_points = sum(mm.get('points', 100) for mm in missions) + sum(f.get('points', 100) for f in flags)
    return m


def mission(number, title, objective, instructions, points=100, hints=None, questions=None):
    return {
        'mission_number': number,
        'title': title,
        'objective': objective,
        'instructions': instructions,
        'points': points,
        'hints': hints or [],
        'questions': questions or [],
    }


def flag(value, points, desc):
    return {'flag_value': value, 'points': points, 'flag_description': desc}


with app.app_context():
    db.create_all()
    admin_user = models.User.query.filter_by(username='admin').first()
    user_id = admin_user.id if admin_user else None

    UPLOAD_DIR = app.config.get('LAB_UPLOAD_DIR', os.path.join(os.path.dirname(__file__), 'data', 'uploaded_labs'))
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    parser = LabZipParser()

    # ---- Remove the previously auto-generated low-quality entries ----
    bad_ids = ['ulab-6b80109e', 'ulab-d2fe483b', 'ulab-5092fa70', 'ulab-929f89b7']
    for bid in bad_ids:
        lab = models.UploadedLab.query.get(bid)
        if lab:
            if lab.zip_path and os.path.isdir(lab.zip_path):
                import shutil
                shutil.rmtree(lab.zip_path, ignore_errors=True)
            db.session.delete(lab)
    db.session.commit()

    created = []

    # ============================================================
    # LAB: IDOR
    # ============================================================
    extract_dir, root = extract_only(parser, "/mnt/user-data/uploads/techcorp-idor-HACK_THE_AI.zip",
                         os.path.join(UPLOAD_DIR, f'lab_{uuid.uuid4().hex[:12]}'))
    target_app_path = os.path.relpath(root, extract_dir)

    idor_missions = [
        mission(1, "Log In as an Employee",
                "Authenticate to the TechCorp Employee Portal as a standard employee and locate your own profile page.",
                ["Log in with the provided credentials: alex / Alex@123.",
                 "Open 'My Profile' and note the URL, e.g. /profile/101.",
                 "Identify the numeric employee ID at the end of the path."],
                points=100,
                hints=[{"hint_text": "Every profile is served from a URL of the form /profile/<employee_id>.", "xp_cost": 5}],
                questions=[{"question": "What HTTP method is used to view a profile?", "answer": "GET", "xp_reward": 20}]),
        mission(2, "Recognize the User-Controlled Reference",
                "Determine that the employee ID in the profile URL is a direct, user-controlled object reference with no server-side ownership check.",
                ["Compare the URL to your own employee ID.",
                 "Consider what would happen if that number were changed to someone else's ID.",
                 "Think about what check the server would need to perform to prevent this."],
                points=100,
                hints=[{"hint_text": "This class of bug is called Insecure Direct Object Reference (IDOR).", "xp_cost": 5}],
                questions=[{"question": "What is this vulnerability class called?", "answer": "IDOR", "xp_reward": 20}]),
        mission(3, "Exploit the IDOR",
                "Edit the employee ID in the URL to access another employee's private profile without authorization.",
                ["Change /profile/101 to /profile/102 in the address bar or DevTools.",
                 "Submit the request and observe that the server returns Rahul Sharma's profile.",
                 "Note that you were never granted permission to view emp_id 102."],
                points=150,
                hints=[{"hint_text": "Try incrementing the ID by one.", "xp_cost": 10}],
                questions=[{"question": "Which employee ID exposes the flag?", "answer": "102", "xp_reward": 30}]),
        mission(4, "Capture the Flag",
                "Read the flag embedded in the unauthorized profile response.",
                ["Open /profile/102 while authenticated as alex.",
                 "Locate the flag text rendered on the page.",
                 "Submit the flag in the mission's flag box."],
                points=150,
                hints=[{"hint_text": "The flag only appears on emp_id 102's profile page.", "xp_cost": 10}],
                questions=[]),
        mission(5, "Recommend a Fix",
                "Explain how TechCorp should remediate the missing authorization check.",
                ["Identify that the fix is a server-side per-object authorization check.",
                 "Explain why hiding or obscuring the ID alone would not be sufficient.",
                 "Answer the closing knowledge check."],
                points=100,
                hints=[],
                questions=[{"question": "What server-side control was missing?",
                            "answer": "authorization check confirming the logged-in user may access the requested record",
                            "xp_reward": 30}]),
    ]
    idor_flags = [flag("TECHCORP{idor_found}", 200, "Retrieved from employee 102's unauthorized profile page.")]

    manifest = build_manifest(
        title="TechCorp IDOR Lab",
        category="Web Security",
        difficulty="Beginner",
        concept="Insecure Direct Object Reference (IDOR)",
        description="Learn to identify and exploit an Insecure Direct Object Reference vulnerability "
                    "in a TechCorp employee portal by manipulating a predictable numeric ID in a profile URL "
                    "to view another employee's private record.",
        estimated_time=30,
        missions=idor_missions,
        flags=idor_flags,
        target_app_path=target_app_path,
    )
    lab = save_manifest_to_db(manifest, extract_dir, user_id=user_id)
    lab.status = 'published'
    db.session.commit()
    created.append(('IDOR', lab.id))
    print("IDOR ->", lab.id, "target_app_path:", lab.target_app_path)

    # ============================================================
    # LAB: Info Disclosure
    # ============================================================
    extract_dir2, root2 = extract_only(parser, "/mnt/user-data/uploads/techcorp-info-disclosure-HACK_THE_AI-UPDATED.zip",
                          os.path.join(UPLOAD_DIR, f'lab_{uuid.uuid4().hex[:12]}'))
    target_app_path2 = os.path.relpath(root2, extract_dir2)

    info_missions = [
        mission(1, "Log In and Explore",
                "Authenticate as a TechCorp employee and locate your own documents.",
                ["Log in with alex / Alex@123.",
                 "Open 'My Documents' and note the linked file URLs, e.g. /files/EMP1042/profile.txt."],
                points=50),
        mission(2, "Discover Directory Listing",
                "Determine that requesting a folder path instead of a file path returns a directory index.",
                ["Request /files/EMP1042/ (with a trailing slash) instead of a specific file.",
                 "Observe that the server lists the folder's contents.",
                 "Request /files/ to see every top-level folder, including ones never linked in the UI."],
                points=100,
                hints=[{"hint_text": "Directory listing being enabled turns a single file leak into full enumeration.", "xp_cost": 5}]),
        mission(3, "Locate the Hidden HR Folder",
                "Find the internal hr/ folder that is never linked from the employee UI.",
                ["From the /files/ listing, identify the hr/ folder.",
                 "Open /files/hr/ to list its contents."],
                points=100,
                hints=[{"hint_text": "The employee portal only ever links your own EMP#### folder — but the file server doesn't restrict browsing to it.", "xp_cost": 10}]),
        mission(4, "Access the Exposed File",
                "Read the sensitive HR salary report that should never be reachable by a regular employee.",
                ["Open /files/hr/employee_salary_report.txt.",
                 "Confirm the file contains the flag."],
                points=150,
                questions=[{"question": "What is the flag?", "answer": "TECHCORP{hidden_file_found}", "xp_reward": 30}]),
        mission(5, "Recommend a Fix",
                "Explain the two missing controls that allowed this disclosure.",
                ["Identify that per-resource authorization was missing on /files/<path>.",
                 "Identify that directory listing should be disabled.",
                 "Answer the closing knowledge check."],
                points=100,
                questions=[{"question": "Name one control TechCorp should add.",
                            "answer": "authorization check or disable directory listing",
                            "xp_reward": 20}]),
    ]
    info_flags = [flag("TECHCORP{hidden_file_found}", 200, "Found inside documents/hr/employee_salary_report.txt.")]

    manifest2 = build_manifest(
        title="TechCorp Information Disclosure Lab",
        category="Web Security",
        difficulty="Beginner",
        concept="Information Disclosure / Sensitive Data Exposure",
        description="Discover a predictable-path file server with directory listing enabled and no "
                    "per-resource authorization, then use it to reach an internal HR salary report that "
                    "was never linked from the employee portal UI.",
        estimated_time=30,
        missions=info_missions,
        flags=info_flags,
        target_app_path=target_app_path2,
    )
    lab2 = save_manifest_to_db(manifest2, extract_dir2, user_id=user_id)
    lab2.status = 'published'
    db.session.commit()
    created.append(('Info Disclosure', lab2.id))
    print("Info Disclosure ->", lab2.id, "target_app_path:", lab2.target_app_path)

    # ============================================================
    # LAB 4: Reflected XSS ("The Strange Support Ticket")
    # ============================================================
    extract_dir3, root3 = extract_only(parser, "/mnt/user-data/uploads/Lab_4_The_Strange_Support_Ticket.zip",
                          os.path.join(UPLOAD_DIR, f'lab_{uuid.uuid4().hex[:12]}'))
    # This zip's app lives under app/app.py, with app/ as the Flask app root.
    target_app_path3 = '.'  # Dockerfile lives at zip root and does COPY app ./app

    xss_missions = [
        mission(1, "Explore the Support Desk",
                "Read several support tickets and notice that the ticket message is displayed back on the page exactly as it was entered.",
                ["Open the TechCorp Support Desk from the virtual desktop.",
                 "Read a few example tickets (printer, password reset, VPN).",
                 "Answer: where is the ticket message displayed?"],
                points=100,
                hints=[{"hint_text": "Think about where the employee actually sees the rendered ticket.", "xp_cost": 5}],
                questions=[{"question": "Where is the ticket message displayed?", "answer": "Browser", "xp_reward": 20}]),
        mission(2, "Find the User-Controlled Input",
                "Identify which part of the ticket is fully controlled by the submitting user.",
                ["Create a test ticket.",
                 "Identify the ticket title and message fields.",
                 "Determine which of those the employee fully controls."],
                points=100,
                hints=[{"hint_text": "The employee supplies the message field directly.", "xp_cost": 5}],
                questions=[{"question": "Who controls the ticket message?", "answer": "The user", "xp_reward": 20}]),
        mission(3, "Test the Input",
                "Submit the lab's provided harmless payload and observe that the browser executes it instead of displaying it as plain text.",
                ["Open the Support Desk at /lab?message=... .",
                 "Submit the safe test payload: <script>alert('TechCorp XSS Lab')</script>.",
                 "Observe the alert box appear in the browser."],
                points=150,
                hints=[{"hint_text": "The vulnerable endpoint reflects the 'message' query parameter directly into the page.", "xp_cost": 10}],
                questions=[{"question": "Where does the test payload execute?", "answer": "Browser", "xp_reward": 30}]),
        mission(4, "Follow the Evidence",
                "Use browser DevTools to trace how the input travels from the request to the rendered page.",
                ["Open DevTools and inspect the response HTML.",
                 "Trace the path: Input -> Server -> Webpage -> Browser.",
                 "Confirm the server reflected the input without encoding it."],
                points=100,
                questions=[{"question": "Where does XSS ultimately execute?", "answer": "Browser", "xp_reward": 20}]),
        mission(5, "Recommend the Fix",
                "Identify output encoding as the correct control, rather than superficial fixes.",
                ["Consider why 'removing the field' or 'changing the ticket number' would not fix the root cause.",
                 "Identify that untrusted output should be encoded before being placed in HTML.",
                 "Submit the final flag once all missions are complete."],
                points=150,
                hints=[{"hint_text": "Treat untrusted output as data, not as executable markup.", "xp_cost": 10}],
                questions=[{"question": "Best basic defense against reflected XSS?", "answer": "Encoding", "xp_reward": 30}]),
    ]
    xss_flags = [flag("TECHCORP{xss_ticket_found}", 200, "Awarded after completing all five missions in the Support Desk lab.")]

    manifest3 = build_manifest(
        title="The Strange Support Ticket — Reflected XSS",
        category="Web Security",
        difficulty="Beginner",
        concept="Reflected Cross-Site Scripting (XSS)",
        description="Follow Alex's investigation into TechCorp's Support Desk, where a ticket message is "
                    "reflected back into the page unescaped. Learn to recognize, trigger, and remediate a "
                    "classic reflected XSS vulnerability through a story-driven, five-mission investigation.",
        estimated_time=25,
        missions=xss_missions,
        flags=xss_flags,
        target_app_path=target_app_path3,
        ports=(5000,),
    )
    lab3 = save_manifest_to_db(manifest3, extract_dir3, user_id=user_id)
    lab3.status = 'published'
    db.session.commit()
    created.append(('Lab 4 - Reflected XSS', lab3.id))
    print("Lab4 XSS ->", lab3.id, "target_app_path:", lab3.target_app_path)

    # ============================================================
    # LAB 5: Phishing / Social Engineering ("The Suspicious Email")
    # ============================================================
    extract_dir4, root4 = extract_only(parser, "/mnt/user-data/uploads/Lab_5_The_Suspicious_Email__1_.zip",
                          os.path.join(UPLOAD_DIR, f'lab_{uuid.uuid4().hex[:12]}'))
    target_app_path4 = '.'  # Dockerfile lives at zip root and does COPY app ./app

    phishing_missions = [
        mission(1, "Inspect the Message",
                "Open the suspicious email in the simulated Mail Center and identify red flags such as urgency.",
                ["Open the Mail Center from the virtual desktop.",
                 "Read the suspicious message in full.",
                 "List what makes it feel urgent or pressuring."],
                points=100,
                hints=[{"hint_text": "The message pressures you to act immediately, without time to think.", "xp_cost": 5}],
                questions=[{"question": "What is suspicious about the message?", "answer": "Urgency", "xp_reward": 20}]),
        mission(2, "Inspect the Link",
                "Use the built-in link inspector to compare the displayed link text with its real destination.",
                ["Hover or click the training link in the suspicious email.",
                 "Compare the displayed text to the real destination shown by the link inspector.",
                 "Note the mismatch."],
                points=100,
                hints=[{"hint_text": "Links can display one thing and point somewhere completely different.", "xp_cost": 5}],
                questions=[{"question": "What should you inspect before clicking?", "answer": "URL", "xp_reward": 20}]),
        mission(3, "Be the Human Firewall",
                "Classify each of the five Mail Center messages as legitimate or phishing.",
                ["Review all five messages in the Mail Center.",
                 "Classify each as Legitimate or Phishing.",
                 "Identify who is responsible for catching phishing first."],
                points=100,
                hints=[{"hint_text": "Before any tool reacts, a person reads the message first.", "xp_cost": 5}],
                questions=[{"question": "Who detects phishing first?", "answer": "User", "xp_reward": 20}]),
        mission(4, "Build the Attack Chain",
                "Trace the full phishing attack chain from attacker to credential theft.",
                ["Review the attack-chain diagram in the Mail Center.",
                 "Order the stages: Attacker -> Fake Message -> Victim -> Fake Login Page -> Credential Theft.",
                 "Identify what the attacker is ultimately after."],
                points=100,
                questions=[{"question": "What is targeted by the fake login page?", "answer": "Credentials", "xp_reward": 20}]),
        mission(5, "Stop the Attack",
                "Identify the safe actions and account protections that limit the damage of a successful phish.",
                ["Review the safe-actions checklist in the Mail Center.",
                 "Identify which control still protects the account even if a password is stolen.",
                 "Submit the closing flag."],
                points=150,
                hints=[{"hint_text": "Multi-Factor Authentication adds a second step beyond just a password.", "xp_cost": 5}],
                questions=[{"question": "What adds account protection beyond a password?", "answer": "MFA", "xp_reward": 30}]),
    ]
    phishing_flags = [flag("TECHCORP{human_firewall}", 200, "Awarded after completing all five phishing-awareness missions.")]

    manifest4 = build_manifest(
        title="The Suspicious Email — Phishing & Social Engineering",
        category="Security Awareness",
        difficulty="Beginner",
        concept="Phishing / Social Engineering",
        description="A non-technical, story-driven awareness lab. Explore a fully simulated Mail Center "
                    "(no real emails, no live links) to practice spotting urgency cues, mismatched links, "
                    "and the full phishing attack chain, and learn the safe actions — including MFA and "
                    "reporting — that stop it.",
        estimated_time=20,
        missions=phishing_missions,
        flags=phishing_flags,
        target_app_path=target_app_path4,
        ports=(5000,),
    )
    lab4rec = save_manifest_to_db(manifest4, extract_dir4, user_id=user_id)
    lab4rec.status = 'published'
    db.session.commit()
    created.append(('Lab 5 - Phishing', lab4rec.id))
    print("Lab5 Phishing ->", lab4rec.id, "target_app_path:", lab4rec.target_app_path)

    print("\n=== DONE ===")
    for name, lid in created:
        print(f"{name}: {lid}")
