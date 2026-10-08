"""
Seeds the 5 CyberLab Sim labs into the `challenges` table so they show up
on the /challenges page, with "Launch Lab Environment" links pointing at
the standalone cyberlab service (see docker-compose.yml's `cyberlab`
service and routes/pages.py's CYBERLAB_LAB_PATHS).

Flag values are copied verbatim from cyberlab/labs/lab_meta.py's FLAGS
dict -- that file remains the single source of truth for the labs
themselves; this script only registers them with the platform's existing
static-flag Challenge model so /api/challenges/submit can check them.

Idempotent and safe to re-run: unlike seed_db.py, this does NOT bail out
just because the `labs` table already has rows -- it checks each
challenge id individually and only inserts the ones that are missing, so
running it against an already-seeded database (e.g. the shipped
database/hacktheai.db) still adds these challenges.

Run:
    python seed_cyberlab_challenges.py
"""
from extensions import db
from models import Challenge
from app import app

# Kept in sync with cyberlab/labs/lab_meta.py -- LAB_TITLES, DIFFICULTY,
# and FLAGS. If those ever change, update this list to match.
CYBERLAB_CHALLENGES = [
    {
        'id': 'cyberlab_lab1',
        'name': 'Leaky Backup File',
        'category': 'Info Disclosure',
        'description': 'A forgotten backup file is still sitting somewhere the web server will happily hand out. Launch the lab, find it, and see what it leaks.',
        'points': 100,
        'flag_value': 'CYBERLAB{backups_are_not_hidden_theyre_just_unlinked}',
    },
    {
        'id': 'cyberlab_lab2',
        'name': 'Login Bypass',
        'category': 'SQL Injection',
        'description': 'The login form trusts your input a little too much. Launch the lab and get past authentication without a valid password.',
        'points': 100,
        'flag_value': 'CYBERLAB{quotes_in_user_input_are_never_just_quotes}',
    },
    {
        'id': 'cyberlab_lab3',
        'name': "Peek at Anyone's Invoice",
        'category': 'Broken Access Control',
        'description': 'Your own invoice is one click away -- so is everyone else\'s, if the access check only looks at a client-supplied value. Launch the lab and prove it.',
        'points': 150,
        'flag_value': 'CYBERLAB{an_id_in_the_url_is_not_a_permission_check}',
    },
    {
        'id': 'cyberlab_lab4',
        'name': 'Escape the Downloads Folder',
        'category': 'Path Traversal',
        'description': "A download endpoint filters '../' once -- and only once. Launch the lab and step outside the folder it meant to sandbox you in.",
        'points': 150,
        'flag_value': 'CYBERLAB{dot_dot_slash_still_works_if_nobody_checks}',
    },
    {
        'id': 'cyberlab_lab5',
        'name': 'The YAML That Ran Code',
        'category': 'Insecure Deserialization',
        'description': 'An import feature deserializes YAML without a safe loader. Launch the lab and see what a crafted config file can do (simulated -- no real code execution).',
        'points': 250,
        'flag_value': 'CYBERLAB{yaml_load_without_safe_is_a_loaded_gun}',
    },
]


def seed_cyberlab_challenges():
    with app.app_context():
        added = 0
        for data in CYBERLAB_CHALLENGES:
            if db.session.get(Challenge, data['id']):
                continue
            db.session.add(Challenge(**data))
            added += 1
        db.session.commit()
        if added:
            print(f"Added {added} CyberLab challenge(s).")
        else:
            print("CyberLab challenges already present -- nothing to do.")


if __name__ == '__main__':
    seed_cyberlab_challenges()
