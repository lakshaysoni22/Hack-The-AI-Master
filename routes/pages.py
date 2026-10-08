from flask import Blueprint, render_template, session, request
from models import Challenge, ChallengeProgress

pages_bp = Blueprint('pages', __name__)

# CyberLab Sim runs as its own Flask service (see docker-compose.yml's
# `cyberlab` service / cyberlab/Dockerfile), not inside this app. These
# challenge ids -> lab paths map the Challenge rows seeded by
# seed_cyberlab_challenges.py to the path each lab lives at inside that
# separate app, so the Challenges page can link straight to it.
CYBERLAB_LAB_PATHS = {
    'cyberlab_lab1': '/lab1/',
    'cyberlab_lab2': '/lab2/',
    'cyberlab_lab3': '/lab3/',
    'cyberlab_lab4': '/lab4/',
    'cyberlab_lab5': '/lab5/',
}
# Host port the cyberlab container is published on (see docker-compose.yml).
CYBERLAB_PORT = 5050


def _cyberlab_launch_urls():
    """Build launch URLs for the CyberLab challenges using the same
    hostname the student's browser is already using to reach this page,
    so it works whether the platform is on localhost or another host --
    only the port differs, since cyberlab is bound to 127.0.0.1 on the
    same machine (see docker-compose.yml comment on the cyberlab service).
    """
    hostname = request.host.split(':')[0]
    return {
        challenge_id: f"http://{hostname}:{CYBERLAB_PORT}{path}"
        for challenge_id, path in CYBERLAB_LAB_PATHS.items()
    }


@pages_bp.route('/')
def index():
    return render_template('landing.html')


@pages_bp.route('/challenges')
def challenges():
    challenges_list = Challenge.query.all()
    completed_ids = []
    if session.get('user_id'):
        user_progress = ChallengeProgress.query.filter_by(user_id=session.get('user_id')).all()
        completed_ids = [p.challenge_id for p in user_progress]

    return render_template(
        'challenges.html',
        title="Challenges",
        challenges=challenges_list,
        completed_ids=completed_ids,
        launch_urls=_cyberlab_launch_urls(),
    )

@pages_bp.route('/docs')
def docs():
    return render_template('docs.html', title="Documentation")

@pages_bp.route('/pricing')
def pricing():
    return render_template('pricing.html', title="Pricing")

@pages_bp.route('/achievements')
def achievements():
    user_id = session.get('user_id')
    completed_missions = set()
    completed_labs = set()
    evidence_count = 0
    total_xp = 0
    
    if user_id:
        from models import MissionProgress, LabProgress, EvidenceProgress
        from services.leaderboard_service import get_leaderboard
        
        mps = MissionProgress.query.filter_by(user_id=user_id, status='COMPLETED').all()
        completed_missions = {mp.mission_id for mp in mps}
        lps = LabProgress.query.filter_by(user_id=user_id, status='COMPLETED').all()
        completed_labs = {lp.lab_id for lp in lps}
        evidence_count = EvidenceProgress.query.filter_by(user_id=user_id, collected=True).count()
        
        leaderboard = get_leaderboard(limit=1000)
        username = session.get('username')
        for row in leaderboard:
            if row['username'] == username:
                total_xp = row['total_xp']
                break

    all_achievements = [
        {
            'id': 'first_blood',
            'title': 'First Blood',
            'description': 'Completed your first investigation mission.',
            'icon': '🎯',
            'unlocked': len(completed_missions) >= 1 or len(completed_labs) >= 1,
            'category': 'Milestone'
        },
        {
            'id': 'ledger_detective',
            'title': 'Ledger Detective',
            'description': 'Investigated destination wallet 0x7C41...9B2D and uncovered on-chain inconsistencies.',
            'icon': '🕵️‍♂️',
            'unlocked': 'lab6_m1' in completed_missions,
            'category': 'Lab 1'
        },
        {
            'id': 'trust_breaker',
            'title': 'Trust Breaker',
            'description': 'Exposed poisoned AI confidence and forged threat intelligence tokens.',
            'icon': '🔓',
            'unlocked': 'lab6_m2' in completed_missions or 'lab6_m3' in completed_missions,
            'category': 'Lab 1'
        },
        {
            'id': 'chain_reconstructor',
            'title': 'Chain Reconstructor',
            'description': 'Reconstructed the full cross-layer attack graph for Case NEX-042.',
            'icon': '⛓️',
            'unlocked': 'lab6_m5' in completed_missions or 'lab6' in completed_labs,
            'category': 'Lab 1'
        },
        {
            'id': 'iot_forensic',
            'title': 'IoT Forensic',
            'description': 'Audited GATEWAY-GW-184 and caught synchronized industrial telemetry tampering.',
            'icon': '📡',
            'unlocked': 'lab7_m1' in completed_missions,
            'category': 'Lab 2'
        },
        {
            'id': 'model_hunter',
            'title': 'Model Hunter',
            'description': 'Deconstructed poisoned training feedback on MODEL-ORION AI sentinel.',
            'icon': '🧠',
            'unlocked': 'lab7_m3' in completed_missions,
            'category': 'Lab 2'
        },
        {
            'id': 'consensus_analyst',
            'title': 'Consensus Analyst',
            'description': 'Prevented consensus partition and resolved validator fork in Case NEX-071.',
            'icon': '⚡',
            'unlocked': 'lab7_m5' in completed_missions or 'lab7' in completed_labs,
            'category': 'Lab 2'
        },
        {
            'id': 'cross_layer_detective',
            'title': 'Cross-Layer Detective',
            'description': 'Mastered multi-vector incident response across Web3, AI, Cybersecurity, and IoT.',
            'icon': '🛡️',
            'unlocked': ('lab6_m5' in completed_missions or 'lab6' in completed_labs) and ('lab7_m5' in completed_missions or 'lab7' in completed_labs),
            'category': 'Mastery'
        },
        {
            'id': 'eagle_eye',
            'title': 'Eagle Eye',
            'description': 'Gathered vital forensic evidence and artifacts across investigation chapters.',
            'icon': '👁️',
            'unlocked': evidence_count >= 3 or len(completed_missions) >= 3,
            'category': 'Forensics'
        },
        {
            'id': 'master_hacker',
            'title': 'Master Hacker',
            'description': 'Demonstrated elite forensic capabilities across the entire platform.',
            'icon': '👑',
            'unlocked': len(completed_missions) >= 8 or total_xp >= 1000,
            'category': 'Elite'
        },
    ]
    
    unlocked_count = sum(1 for a in all_achievements if a['unlocked'])
    
    return render_template(
        'achievements.html',
        title="Achievements",
        achievements=all_achievements,
        unlocked_count=unlocked_count,
        total_count=len(all_achievements)
    )

@pages_bp.route('/learning')
def learning():
    user_id = session.get('user_id')
    completed_missions = set()
    if user_id:
        from models import MissionProgress
        mps = MissionProgress.query.filter_by(user_id=user_id, status='COMPLETED').all()
        completed_missions = {mp.mission_id for mp in mps}

    tracks = [
        {
            'title': 'Web3 & Blockchain Security',
            'description': 'Master on-chain forensics, wallet provenance, smart contract policy engines, and decentralized state verification.',
            'icon': '⛓️',
            'badge': 'Web3',
            'missions': ['lab6_m1', 'lab6_m5', 'lab7_m2', 'lab7_m4'],
            'topics': ['Wallet Analysis & Nonce Tracking', 'Oracle Manipulation & Aggregation', 'Validator Consensus & Fork Detection', 'On-chain Event Tracing']
        },
        {
            'title': 'AI & Neural Sentinel Security',
            'description': 'Investigate AI decision auditing, poisoned context injection, confidence score spoofing, and adversarial feedback loops.',
            'icon': '🧠',
            'badge': 'AI Security',
            'missions': ['lab6_m2', 'lab6_m4', 'lab7_m3'],
            'topics': ['AI Confidence Threshold Bypass', 'Poisoned Knowledge Bases (RAG/Intel)', 'Adversarial Training Feedback', 'Automated Decision Hijacking']
        },
        {
            'title': 'IoT & Industrial Telemetry Forensics',
            'description': 'Analyze edge device sensor streams, gateway aggregation spoofing, and synchronized variance anomalies.',
            'icon': '📡',
            'badge': 'IoT Security',
            'missions': ['lab7_m1', 'lab7_m2'],
            'topics': ['Industrial Gateway Log Auditing', 'Telemetry Frequency & Timestamp Tampering', 'Sensor Data Spoofing', 'Edge-to-Cloud Pipeline Security']
        },
        {
            'title': 'Application Security & Identity (RBAC/CSRF)',
            'description': 'Uncover forged admin session tokens, CSRF validation failures, cookie attribute tampering, and API authorization flaws.',
            'icon': '🛡️',
            'badge': 'Cybersecurity',
            'missions': ['lab6_m3', 'lab6_m4'],
            'topics': ['Threat Intel Ingestion Hardening', 'Session Hijacking & Cookie Forensics', 'RBAC Permission Escalation', 'Policy Engine Ruleset Verification']
        },
        {
            'title': 'Consensus Security & Cross-Layer Response',
            'description': 'Perform multi-layer triage connecting physical telemetry to AI, oracles, blockchain state, and governance restoration.',
            'icon': '⚡',
            'badge': 'Incident Response',
            'missions': ['lab7_m4', 'lab7_m5', 'lab6_m5'],
            'topics': ['Validator Partition Diagnostics', 'Attack Graph Reconstruction', 'Emergency Governance Proposals', 'Cross-Layer Containment Protocols']
        }
    ]

    learning_paths = []
    for track in tracks:
        total = len(track['missions'])
        completed = sum(1 for m in track['missions'] if m in completed_missions)
        pct = int((completed / total) * 100) if total > 0 else 0
        learning_paths.append({
            'title': track['title'],
            'description': track['description'],
            'icon': track['icon'],
            'badge': track['badge'],
            'topics': track['topics'],
            'total_missions': total,
            'completed_missions': completed,
            'percentage': pct,
            'status': 'Completed' if pct == 100 else ('In Progress' if pct > 0 else 'Not Started')
        })

    return render_template('learning.html', title="Learning", learning_paths=learning_paths)

@pages_bp.route('/profile')
def profile():
    from services.leaderboard_service import get_leaderboard
    
    stats = {
        'total_xp': 0,
        'labs_completed': 0,
        'missions_completed': 0,
        'rank': 'N/A'
    }
    
    if session.get('user_id'):
        username = session.get('username')
        leaderboard = get_leaderboard(limit=1000)
        for index, row in enumerate(leaderboard):
            if row['username'] == username:
                stats['total_xp'] = row['total_xp']
                stats['labs_completed'] = row['labs_completed']
                stats['missions_completed'] = row['missions_completed']
                stats['rank'] = f"#{index + 1}"
                break
                
    return render_template('profile.html', stats=stats)
