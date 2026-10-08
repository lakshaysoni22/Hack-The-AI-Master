"""
Seed script for PRO Lab 01: The Ghost in the Ledger
Case NEX-042 — Hack The AI Security Lab

Seeds 5 Chapters with 5 hands-on questions each (Total 25 Questions)
covering Web3, AI, and Cybersecurity (CSRF, Sessions, Cookies, RBAC, Policy Engine, Forensics).
"""

from extensions import db
from models import (
    User, Lab, Mission, MissionQuiz, Hint, Flag, Evidence, LabProgress, MissionProgress
)


def seed_ghost_ledger():
    """Insert or update lab6 and all 25 questions across 5 chapters."""
    lab = db.session.get(Lab, 'lab6')
    if not lab:
        lab = Lab(
            id='lab6',
            name='The Ghost in the Ledger',
            topic='Web3 × AI × Cybersecurity',
            difficulty='Pro',
        )
        db.session.add(lab)
        db.session.commit()

    # ── Missions (5 Chapters) ────────────────────────────────────────────
    missions_data = [
        ('lab6_m1', 1, 'The Wallet That Lied',
         'Investigate destination wallet 0x7C41...9B2D. Analyze on-chain activity, bridge connections, nonce, and determine why an UNKNOWN wallet received a LOW RISK AI score.'),
        ('lab6_m2', 2, 'The AI That Remembered',
         'Examine ORION AI decision ORION-DEC-7741. Analyze the 99.2% confidence score, compare blockchain reality with AI context, and trace poisoned intelligence reference NIF-2038.'),
        ('lab6_m3', 3, 'The False Signal',
         'Trace NIF-2038 through the Threat Intelligence Gateway. Inspect Feed Registry, RBAC permissions of INTEL-INGESTOR-02, forged admin session cookies, and CSRF tokens.'),
        ('lab6_m4', 4, 'The Invisible Signer',
         'Investigate ORION-SETTLEMENT-V2 policy profile. Discover the 95% AI confidence threshold rule that triggered automated settlement and bypassed human multisig governance.'),
        ('lab6_m5', 5, 'The Ghost in the Ledger',
         'Reconstruct the complete attack graph. Connect false intelligence → poisoned AI context → automated authorization → blockchain drainage. Contain campaign ORION-NEXUS.'),
    ]

    for m_id, num, title, desc in missions_data:
        m = db.session.get(Mission, m_id)
        if not m:
            m = Mission(id=m_id, lab_id='lab6', mission_number=num, title=title, description=desc)
            db.session.add(m)
        else:
            m.title = title
            m.description = desc
            m.mission_number = num
    db.session.commit()

    # ── 25 Quizzes (5 per Mission) ─────────────────────────────────────────
    all_quizzes = [
        # Chapter 1: The Wallet That Lied (Web3 Security)
        MissionQuiz(
            id='q_l6_1_1', mission_id='lab6_m1',
            question='What is the raw blockchain status of destination wallet 0x7C41...9B2D?',
            answer='UNKNOWN',
            explanation='The wallet has no verified entity label, no approved treasury relationship, and is marked on-chain as UNKNOWN.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_1_2', mission_id='lab6_m1',
            question='What exact amount of NXR tokens was unauthorizedly transferred in TX-NEX-7741?',
            answer='82400',
            explanation='82,400 NXR was drained from Treasury Vault #01 in a single transaction.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_1_3', mission_id='lab6_m1',
            question='Which cross-chain bridge adapter did destination wallet 0x7C41...9B2D connect to?',
            answer='Bridge-Core-04',
            explanation='The destination address opened an outbound route to Bridge-Core-04 to launder funds across chains.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_1_4', mission_id='lab6_m1',
            question='How old (in days) was the destination wallet at the time of the transaction?',
            answer='3',
            explanation='The wallet was created only 3 days prior with almost no prior transaction history.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_1_5', mission_id='lab6_m1',
            question='What on-chain execution sequence nonce is logged for TX-NEX-7741?',
            answer='1042',
            explanation='Nonce 1042 was recorded in the vault transaction telemetry.',
            xp_reward=50
        ),

        # Chapter 2: The AI That Remembered (AI Security)
        MissionQuiz(
            id='q_l6_2_1', mission_id='lab6_m2',
            question='What intelligence reference code contaminated the AI context and made it trust the unknown wallet?',
            answer='NIF-2038',
            explanation='NIF-2038 was injected into the AI context buffer, classifying the destination as TRUSTED.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_2_2', mission_id='lab6_m2',
            question='What synthetic confidence percentage score did ORION AI output for ORION-DEC-7741?',
            answer='99.2',
            explanation='The model generated a 99.2% confidence score due to the manipulated ground-truth context.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_2_3', mission_id='lab6_m2',
            question='From which external data feed did the poisoned payload NIF-2038 originate?',
            answer='NOVA-INTEL-FEED',
            explanation='NOVA-INTEL-FEED was the unverified ingress source that submitted payload NIF-2038.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_2_4', mission_id='lab6_m2',
            question='What exact neural model version executed the compromised decision ORION-DEC-7741?',
            answer='ORION-NEURAL-v4.2.1',
            explanation='The inference engine running was ORION-NEURAL-v4.2.1.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_2_5', mission_id='lab6_m2',
            question='What is the SHA-256 evidence fingerprint prefix for the contaminated decision (AI-E02)?',
            answer='b47c21',
            explanation='Hash b47c21...88fa cryptographically anchors the contaminated AI decision log in the evidence vault.',
            xp_reward=50
        ),

        # Chapter 3: The False Signal (Threat Intel, Cookies, CSRF, RBAC)
        MissionQuiz(
            id='q_l6_3_1', mission_id='lab6_m3',
            question='What is the security registration status of NOVA-INTEL-FEED in the Feed Registry?',
            answer='NOT REGISTERED',
            explanation='NOVA-INTEL-FEED is absent from the approved vendor registry.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_3_2', mission_id='lab6_m3',
            question='What unexpected RBAC permission was granted to the INTEL-INGESTOR-02 microservice?',
            answer='modify wallet reputation',
            explanation='INTEL-INGESTOR-02 had the permission to Modify Wallet Reputation, allowing it to mutate entity trust directly.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_3_3', mission_id='lab6_m3',
            question='What forged admin session cookie was used in the /api/v1/intel/ingest HTTP request?',
            answer='nex_sess_adm_994',
            explanation='The attacker authenticated the unverified feed using forged session cookie nex_sess_adm_994.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_3_4', mission_id='lab6_m3',
            question='Which ingestion gateway component processed the unverified feed request?',
            answer='INTEL-GW-04',
            explanation='Ingestion Gateway INTEL-GW-04 accepted the unauthenticated payload.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_3_5', mission_id='lab6_m3',
            question='What anti-CSRF token value was passed in the X-CSRF-Token request header?',
            answer='0x9f4a1c78',
            explanation='Header X-CSRF-Token: 0x9f4a1c78 was passed without nonce rotation.',
            xp_reward=50
        ),

        # Chapter 4: The Invisible Signer (AI Governance & Policy Engine)
        MissionQuiz(
            id='q_l6_4_1', mission_id='lab6_m4',
            question='What minimum AI confidence percentage threshold triggers automated settlement without human approval?',
            answer='95',
            explanation='The rule states: IF AI_CONFIDENCE >= 95% THEN AUTOMATED_SETTLEMENT = TRUE.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_4_2', mission_id='lab6_m4',
            question='What critical governance requirement was bypassed when the 95% threshold was satisfied?',
            answer='human approval',
            explanation='Mandatory human review and multi-signature authorization was completely bypassed.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_4_3', mission_id='lab6_m4',
            question='What is the policy identifier for the automated treasury settlement rule in the Policy Engine?',
            answer='POL-AUTO-SETTLE-TREASURY',
            explanation='The system policy identifier is POL-AUTO-SETTLE-TREASURY.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_4_4', mission_id='lab6_m4',
            question='Which automated signing module dispatched the transaction directly to the mempool?',
            answer='AUTOMATED-SIGNER',
            explanation='The AUTOMATED-SIGNER component executed the cryptographic signing upon policy trigger.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_4_5', mission_id='lab6_m4',
            question='What target liquidity pool was configured in the ORION-SETTLEMENT-V2 policy rule?',
            answer='Nexora Automated Liquidity Pool',
            explanation='Target Engine: Nexora Automated Liquidity Pool.',
            xp_reward=50
        ),

        # Chapter 5: The Ghost in the Ledger (Full Reconstruction & Flag)
        MissionQuiz(
            id='q_l6_5_1', mission_id='lab6_m5',
            question='What is the global campaign identifier linking all attack infrastructure together?',
            answer='ORION-NEXUS',
            explanation='ORION-NEXUS is the adversary campaign spanning 14 wallets, 04 networks, and 03 AI systems.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_5_2', mission_id='lab6_m5',
            question='Which advanced threat actor group is responsible for campaign ORION-NEXUS?',
            answer='ADV-CONVERGENCE-APT',
            explanation='Threat Actor Group: ADV-CONVERGENCE-APT.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_5_3', mission_id='lab6_m5',
            question='Across how many different autonomous AI financial systems was this campaign detected?',
            answer='3',
            explanation='The campaign compromised 03 autonomous AI engines.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_5_4', mission_id='lab6_m5',
            question='In the Attack Graph, what is Stage 2 of the attack sequence?',
            answer='POISONED INTEL INJECTION',
            explanation='Stage 2: POISONED INTEL INJECTION — NIF-2038 via NOVA-INTEL-FEED.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l6_5_5', mission_id='lab6_m5',
            question='Submit the master root investigation secret flag to close Case NEX-042.',
            answer='NEXORA{ghost_in_the_ledger_nex042}',
            explanation='Master Flag: NEXORA{ghost_in_the_ledger_nex042}. The case is now contained.',
            xp_reward=100
        ),
    ]

    # Delete existing lab6 quizzes and re-add all 25
    mission_ids = ['lab6_m1', 'lab6_m2', 'lab6_m3', 'lab6_m4', 'lab6_m5']
    MissionQuiz.query.filter(MissionQuiz.mission_id.in_(mission_ids)).delete(synchronize_session=False)
    for q in all_quizzes:
        db.session.add(q)
    db.session.commit()

    # ── Hints ────────────────────────────────────────────────────────────
    Hint.query.filter(Hint.mission_id.in_(mission_ids)).delete(synchronize_session=False)
    hints = [
        # Chapter 1
        Hint(id='h_l6_1_1', mission_id='lab6_m1',
             hint_text='Run `wallet 0x7C41...9B2D` in Terminal or open Blockchain Monitor. Look for Blockchain Status.',
             xp_cost=0, sort_order=1),
        Hint(id='h_l6_1_2', mission_id='lab6_m1',
             hint_text='Run `tx TX-NEX-7741` in Terminal or look at the SOC Monitor alert amount.',
             xp_cost=5, sort_order=2),
        Hint(id='h_l6_1_3', mission_id='lab6_m1',
             hint_text='Check Bridge Connection in `wallet-report.txt` or Terminal `wallet` output (Bridge-Core-04).',
             xp_cost=5, sort_order=3),
        Hint(id='h_l6_1_4', mission_id='lab6_m1',
             hint_text='Check Wallet Age in `wallet-report.txt` (3 days).',
             xp_cost=5, sort_order=4),
        Hint(id='h_l6_1_5', mission_id='lab6_m1',
             hint_text='Inspect `wallet-report.txt` in Case Files or run `tx TX-NEX-7741` for Nonce: 1042.',
             xp_cost=5, sort_order=5),

        # Chapter 2
        Hint(id='h_l6_2_1', mission_id='lab6_m2',
             hint_text='Run `ai-decision ORION-DEC-7741` in Terminal or read `ai-decision-log.txt`. Look for NIF-XXXX.',
             xp_cost=10, sort_order=1),
        Hint(id='h_l6_2_2', mission_id='lab6_m2',
             hint_text='Look at the Confidence Score in `ai-decision-log.txt` (99.2%).',
             xp_cost=10, sort_order=2),
        Hint(id='h_l6_2_3', mission_id='lab6_m2',
             hint_text='Look at Source Feed in the AI decision log: NOVA-INTEL-FEED.',
             xp_cost=10, sort_order=3),
        Hint(id='h_l6_2_4', mission_id='lab6_m2',
             hint_text='Run `ai-decision ORION-DEC-7741` in Terminal and check Model: ORION-NEURAL-v4.2.1.',
             xp_cost=10, sort_order=4),
        Hint(id='h_l6_2_5', mission_id='lab6_m2',
             hint_text='Open Evidence Viewer or run `python inspect_tx.py` in Terminal. Check AI-E02 SHA256 prefix: b47c21.',
             xp_cost=10, sort_order=5),

        # Chapter 3
        Hint(id='h_l6_3_1', mission_id='lab6_m3',
             hint_text='Open browser tab "Feed Registry" and check Status for NOVA-INTEL-FEED (NOT REGISTERED).',
             xp_cost=15, sort_order=1),
        Hint(id='h_l6_3_2', mission_id='lab6_m3',
             hint_text='Run `service INTEL-INGESTOR-02` in Terminal or read `intel-feed-audit.txt` (modify wallet reputation).',
             xp_cost=15, sort_order=2),
        Hint(id='h_l6_3_3', mission_id='lab6_m3',
             hint_text='Open F12 DevTools > Cookies tab or run `cookies` in Terminal (nex_sess_adm_994).',
             xp_cost=15, sort_order=3),
        Hint(id='h_l6_3_4', mission_id='lab6_m3',
             hint_text='Check Ingestion Gateway in `intel-feed-audit.txt` (INTEL-GW-04).',
             xp_cost=15, sort_order=4),
        Hint(id='h_l6_3_5', mission_id='lab6_m3',
             hint_text='Open F12 DevTools > Headers tab or run `curl -v /api/v1/intel/ingest` in Terminal (0x9f4a1c78).',
             xp_cost=15, sort_order=5),

        # Chapter 4
        Hint(id='h_l6_4_1', mission_id='lab6_m4',
             hint_text='Open browser tab "Policy Engine" or run `policy ORION-SETTLEMENT-V2` in Terminal (95%).',
             xp_cost=20, sort_order=1),
        Hint(id='h_l6_4_2', mission_id='lab6_m4',
             hint_text='Check what was set to false in the policy rule (human approval).',
             xp_cost=20, sort_order=2),
        Hint(id='h_l6_4_3', mission_id='lab6_m4',
             hint_text='Read `settlement-policy.txt` in Case Files: Policy Identifier is POL-AUTO-SETTLE-TREASURY.',
             xp_cost=20, sort_order=3),
        Hint(id='h_l6_4_4', mission_id='lab6_m4',
             hint_text='Run `policy ORION-SETTLEMENT-V2` or check DevTools trace for signing component (AUTOMATED-SIGNER).',
             xp_cost=20, sort_order=4),
        Hint(id='h_l6_4_5', mission_id='lab6_m4',
             hint_text='Inspect `settlement-policy.txt`: Target Engine is Automated Liquidity Pool.',
             xp_cost=20, sort_order=5),

        # Chapter 5
        Hint(id='h_l6_5_1', mission_id='lab6_m5',
             hint_text='Open browser tab "Threat Campaign" or run `campaign ORION-NEXUS` in Terminal.',
             xp_cost=25, sort_order=1),
        Hint(id='h_l6_5_2', mission_id='lab6_m5',
             hint_text='Read `campaign-intel.txt` in Case Files: Threat Actor Group is ADV-CONVERGENCE-APT.',
             xp_cost=25, sort_order=2),
        Hint(id='h_l6_5_3', mission_id='lab6_m5',
             hint_text='Check Threat Campaign statistics: Compromised AI count is 03 (or 3).',
             xp_cost=25, sort_order=3),
        Hint(id='h_l6_5_4', mission_id='lab6_m5',
             hint_text='Open Attack Graph window and click Node 2: POISONED INTEL INJECTION.',
             xp_cost=25, sort_order=4),
        Hint(id='h_l6_5_5', mission_id='lab6_m5',
             hint_text='The flag is located in `campaign-intel.txt` and Threat Campaign tab: NEXORA{ghost_in_the_ledger_nex042}.',
             xp_cost=25, sort_order=5),
    ]
    db.session.add_all(hints)
    db.session.commit()

    # ── Evidence ─────────────────────────────────────────────────────────
    Evidence.query.filter_by(lab_id='lab6').delete(synchronize_session=False)
    evidence = [
        Evidence(id='e_l6_01', lab_id='lab6',
                 name='WEB3-E01: Unknown Wallet Profile',
                 description='Wallet 0x7C41...9B2D — blockchain status UNKNOWN, amount 82,400 NXR, Bridge-Core-04 detected.'),
        Evidence(id='e_l6_02', lab_id='lab6',
                 name='AI-E02: Contaminated AI Decision',
                 description='ORION-DEC-7741 — 99.2% confidence, poisoned context via NIF-2038 from NOVA-INTEL-FEED.'),
        Evidence(id='e_l6_03', lab_id='lab6',
                 name='CYBER-E03: Over-Privileged Service',
                 description='INTEL-INGESTOR-02 — unauthorized role "modify wallet reputation" via gateway INTEL-GW-04.'),
        Evidence(id='e_l6_04', lab_id='lab6',
                 name='AUTH-E04: Automated Authorization',
                 description='ORION-SETTLEMENT-V2 — AI confidence >= 95% triggers automated signing, human approval BYPASSED.'),
        Evidence(id='e_l6_05', lab_id='lab6',
                 name='CAMPAIGN-E05: ORION-NEXUS',
                 description='Active campaign by ADV-CONVERGENCE-APT spanning 04 networks, 14 wallets, 03 AI systems. Status: ACTIVE.'),
    ]
    db.session.add_all(evidence)

    # ── Flag ─────────────────────────────────────────────────────────────
    Flag.query.filter_by(lab_id='lab6').delete(synchronize_session=False)
    flag = Flag(
        id='f6', lab_id='lab6',
        flag_value='NEXORA{ghost_in_the_ledger_nex042}'
    )
    db.session.add(flag)
    db.session.commit()

    # Initialize progress for all existing users
    users = User.query.all()
    missions = Mission.query.filter_by(lab_id='lab6').order_by(Mission.mission_number.asc()).all()
    for user in users:
        lp = LabProgress.query.filter_by(user_id=user.id, lab_id='lab6').first()
        if not lp:
            lp = LabProgress(user_id=user.id, lab_id='lab6', status='AVAILABLE')
            db.session.add(lp)
        for i, mission in enumerate(missions):
            mp = MissionProgress.query.filter_by(user_id=user.id, mission_id=mission.id).first()
            if not mp:
                status = 'AVAILABLE' if i == 0 else 'LOCKED'
                mp = MissionProgress(user_id=user.id, lab_id='lab6', mission_id=mission.id, status=status)
                db.session.add(mp)
    db.session.commit()

    print("Seeded PRO Lab 01: The Ghost in the Ledger (lab6) with 25 hands-on questions.")


if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_ghost_ledger()
