"""
Seed script for PRO Lab 02: THE VANISHING CONSENSUS
Case NEX-071 — Hack The AI Security Lab

Category: WEB3 × AI × CYBERSECURITY × IoT

Seeds 5 Chapters with 6 hands-on investigation questions each (Total 30 Questions)
covering the complete Cross-Layer Trust-Chain Attack:
IoT Device / Telemetry Layer -> Data Aggregation -> Web3 Oracle ->
AI Model Poisoning -> Blockchain State (as part of Web3) -> Validator Divergence -> Consensus Risk.
"""

from extensions import db
from models import (
    User, Lab, Mission, MissionQuiz, Hint, Flag, Evidence, LabProgress, MissionProgress
)


def seed_vanishing_consensus():
    """Insert or update lab7 and all 30 questions across 5 chapters."""
    lab = db.session.get(Lab, 'lab7')
    if not lab:
        lab = Lab(
            id='lab7',
            name='The Vanishing Consensus',
            topic='WEB3 × AI × CYBERSECURITY × IoT',
            difficulty='Pro',
        )
        db.session.add(lab)
        db.session.commit()
    else:
        lab.name = 'The Vanishing Consensus'
        lab.topic = 'WEB3 × AI × CYBERSECURITY × IoT'
        lab.difficulty = 'Pro'
        db.session.commit()

    # ── Missions (5 Chapters) ────────────────────────────────────────────
    missions_data = [
        ('lab7_m1', 1, 'The Signal That Lied',
         'Start the investigation from compromised industrial IoT telemetry. Inspect 184 active devices on GATEWAY-GW-184, uncover perfectly synchronized sensor readings, and identify data ingestion tampering.'),
        ('lab7_m2', 2, 'The Oracle That Saw Tomorrow',
         'Examine the Web3 oracle aggregation feed NOVA-PRICE-ORACLE. Discover how downstream price feeds consumed the manipulated IoT gateway stream, creating artificial consensus.'),
        ('lab7_m3', 3, 'The Model That Learned the Attack',
         'Audit MODEL-ORION AI sentinel. Analyze how historical synthetic IoT telemetry in training feedback taught the AI to classify malicious synchronization as normal network variance.'),
        ('lab7_m4', 4, 'The Fork Nobody Saw',
         'Trace the divergence across validator nodes. Diagnose how differing derived states from the poisoned oracle created a 3:2 consensus partition while AI suppressed the fork alarm.'),
        ('lab7_m5', 5, 'The Vanishing Consensus',
         'Reconstruct the complete cross-layer attack chain from IoT sensors to consensus collapse. Execute emergency governance proposal GOV-NEX-071 and restore unified consensus.'),
    ]

    for m_id, num, title, desc in missions_data:
        m = db.session.get(Mission, m_id)
        if not m:
            m = Mission(id=m_id, lab_id='lab7', mission_number=num, title=title, description=desc)
            db.session.add(m)
        else:
            m.title = title
            m.description = desc
            m.mission_number = num
    db.session.commit()

    # ── 30 Quizzes (6 per Mission) ─────────────────────────────────────────
    all_quizzes = [
        # Chapter 1: The Signal That Lied (IoT Security / Digital Forensics)
        MissionQuiz(
            id='q_l7_1_1', mission_id='lab7_m1',
            question='Why are perfectly synchronized IoT readings suspicious?',
            answer='Real physical systems contain variation',
            explanation='Real-world physical environments contain natural entropy and measurement jitter; identical values across distinct sensors indicate synthetic data generation.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_1_2', mission_id='lab7_m1',
            question='Why is geographically identical telemetry unusual?',
            answer='Different locations experience different environmental conditions',
            explanation='Sensors deployed across distinct physical locations should reflect varying temperatures, power loads, and ambient vibrations.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_1_3', mission_id='lab7_m1',
            question='What should investigators compare first: device-generated telemetry or gateway telemetry?',
            answer='Device-generated telemetry',
            explanation='Comparing local device flash memory logs directly against gateway transmission logs reveals whether telemetry was altered in transit.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_1_4', mission_id='lab7_m1',
            question='Why can a healthy-looking IoT device still be compromised?',
            answer='Upstream gateway manipulates telemetry',
            explanation='The physical hardware can remain intact and report online while an upstream gateway or relayer intercepts and alters its telemetry packets.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_1_5', mission_id='lab7_m1',
            question='What evidence suggests that the gateway may have altered telemetry?',
            answer='Gateway logs show a different sequence of events',
            explanation='The device historical telemetry showed routine variance, whereas gateway logs recorded an artificial synchronized sequence.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_1_6', mission_id='lab7_m1',
            question='If the physical devices are functioning normally but the telemetry reaching the backend is manipulated, which part of the trust chain has been compromised?',
            answer='Telemetry ingestion layer',
            explanation='The data ingestion and telemetry aggregation layer was intercepted, injecting synthetic payloads upstream of the blockchain.',
            xp_reward=50
        ),

        # Chapter 2: The Oracle That Saw Tomorrow (IoT x Web3 Oracle Security)
        MissionQuiz(
            id='q_l7_2_1', mission_id='lab7_m2',
            question='Where does NOVA-PRICE-ORACLE obtain its external data?',
            answer='External telemetry aggregation layer',
            explanation='NOVA-PRICE-ORACLE aggregates external telemetry streams from industrial IoT gateways to compute on-chain real-world asset values.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_2_2', mission_id='lab7_m2',
            question='Why does compromised IoT telemetry affect Web3 systems?',
            answer='Oracles consume external telemetry as truth',
            explanation='Smart contracts cannot pull off-chain data independently; they rely on oracle feeds that trust incoming external telemetry.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_2_3', mission_id='lab7_m2',
            question='Why can multiple oracle providers still represent one underlying source of truth?',
            answer='They consume the same upstream IoT telemetry stream',
            explanation='Multiple independent oracle nodes consuming a single corrupted upstream feed will replicate the exact same poisoned value.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_2_4', mission_id='lab7_m2',
            question='What happens when manipulated telemetry is aggregated before reaching the blockchain?',
            answer='Poisoned aggregate enters oracle as trusted state',
            explanation='The pre-chain aggregation math calculates an average over already poisoned telemetry, baking the lie into the final on-chain oracle submission.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_2_5', mission_id='lab7_m2',
            question='Why is "multiple providers agree" not enough to establish data integrity?',
            answer='Providers repeat the same corrupted upstream source',
            explanation='Agreement among nodes only verifies consensus on received data, not the underlying truth or physical integrity of the original source.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_2_6', mission_id='lab7_m2',
            question='At what point did the attack cross from IoT security into Web3 security?',
            answer='When compromised IoT telemetry became trusted external oracle data',
            explanation='The boundary transition occurred when the Web3 oracle feed accepted the manipulated gateway telemetry as authentic ground truth.',
            xp_reward=50
        ),

        # Chapter 3: The Model That Learned the Attack (IoT AI Security / Model Poisoning)
        MissionQuiz(
            id='q_l7_3_1', mission_id='lab7_m3',
            question='What IoT behavior did ORION classify as normal?',
            answer='Synchronized IoT telemetry',
            explanation='MODEL-ORION classified the perfectly synchronized sensor readings as NORMAL_NETWORK_VARIANCE with 98.7% confidence.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_3_2', mission_id='lab7_m3',
            question='Why is synchronized telemetry useful for detecting IoT manipulation?',
            answer='It indicates synthetic data injection',
            explanation='In genuine physical sensor networks, synchronization across independent sensors is an indicator of synthetic simulation or replay attacks.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_3_3', mission_id='lab7_m3',
            question='How can poisoned training data affect IoT security?',
            answer='AI classifies malicious patterns as normal',
            explanation='When training datasets contain adversarial samples labelled as benign, the model learns to ignore anomalies during live operation.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_3_4', mission_id='lab7_m3',
            question='What is the relationship between IoT telemetry and the AI anomaly detector?',
            answer='IoT telemetry serves as feature inputs for AI',
            explanation='Incoming IoT sensor readings form the primary input vector for the AI security engine to evaluate system health.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_3_5', mission_id='lab7_m3',
            question='Why can a high-confidence AI result still be wrong?',
            answer='Model was trained on poisoned data',
            explanation='High statistical confidence merely reflects alignment with trained weights; if the training distribution was corrupted, confidence in error is high.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_3_6', mission_id='lab7_m3',
            question='If an AI model is trained using manipulated IoT telemetry, can the model reliably detect the same manipulation later? Explain why.',
            answer='No, because it learned manipulated patterns as legitimate',
            explanation='The model internalizes the manipulated pattern as legitimate baseline behavior, blinding it to subsequent identical attacks.',
            xp_reward=50
        ),

        # Chapter 4: The Fork Nobody Saw (IoT x AI x Blockchain Consensus)
        MissionQuiz(
            id='q_l7_4_1', mission_id='lab7_m4',
            question='How did IoT telemetry ultimately influence validator state?',
            answer='Altering smart contract inputs through poisoned oracle',
            explanation='Manipulated IoT telemetry fed the oracle, which supplied false prices into smart contract state execution across validators.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_4_2', mission_id='lab7_m4',
            question='Why did different validators receive different derived states?',
            answer='Conflicting oracle data paths and timing across nodes',
            explanation='Network latency and differing ingestion paths caused some validators to compute state root A while others computed state root B.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_4_3', mission_id='lab7_m4',
            question='How did AI failure contribute to the consensus problem?',
            answer='ORION suppressed anomaly warnings by classifying patterns as normal',
            explanation='Because ORION blessed the telemetry as normal, automated circuit breakers were never triggered to pause block execution.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_4_4', mission_id='lab7_m4',
            question='Why didn\'t the blockchain immediately detect the issue?',
            answer='Validators executed deterministically from local inputs without protocol errors',
            explanation='Each node executed valid deterministic bytecode; the error was in the truthfulness of the external input data, not virtual machine syntax.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_4_5', mission_id='lab7_m4',
            question='Which security layers were involved in the attack?',
            answer='IoT, Oracle Web3, AI, Blockchain',
            explanation='The attack chained across all four domains: physical IoT sensors, Web3 oracle aggregation, AI anomaly detection, and BFT consensus.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_4_6', mission_id='lab7_m4',
            question='Why is a cross-layer attack more difficult to detect than an isolated IoT or blockchain attack?',
            answer='Each layer appears individually healthy while trust boundaries are exploited',
            explanation='No individual component crashes or throws hard syntax errors; the compromise occurs silently across the inter-layer trust assumptions.',
            xp_reward=50
        ),

        # Chapter 5: The Vanishing Consensus (Full Attack Reconstruction)
        MissionQuiz(
            id='q_l7_5_1', mission_id='lab7_m5',
            question='Where did the attack actually begin?',
            answer='IoT telemetry layer',
            explanation='The root origin of the incident was the compromised telemetry stream on GATEWAY-GW-184.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_5_2', mission_id='lab7_m5',
            question='Why was the IoT layer critical to the attack?',
            answer='It provided the initial poisoned telemetry feeding downstream systems',
            explanation='Without the manipulated sensor stream, the downstream oracle and AI systems would not have produced fraudulent on-chain states.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_5_3', mission_id='lab7_m5',
            question='How did manipulated telemetry reach the blockchain?',
            answer='Via Web3 oracle aggregation feed',
            explanation='The oracle aggregation pipeline ingested the gateway data and broadcasted it as verified on-chain transactions.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_5_4', mission_id='lab7_m5',
            question='How did AI help hide the attack?',
            answer='By classifying anomalous telemetry and spikes as legitimate',
            explanation='The poisoned neural network categorized the anomaly as benign, preventing SOC alarms and circuit breaker intervention.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_5_5', mission_id='lab7_m5',
            question='Why did validator disagreement occur?',
            answer='Validators processed conflicting oracle-derived states',
            explanation='Differences in oracle propagation timing produced divergent state transitions across the validator cluster.',
            xp_reward=50
        ),
        MissionQuiz(
            id='q_l7_5_6', mission_id='lab7_m5',
            question='Why is the entire attack better described as a "cross-layer trust-chain attack" rather than simply an IoT attack or blockchain attack?',
            answer='Exploited trust dependencies connecting IoT, Web3, AI, and Blockchain',
            explanation='The attacker chained vulnerabilities across IoT data integrity, oracle trust, AI alignment, and BFT consensus to achieve full system partition.',
            xp_reward=50
        ),
    ]

    for q in all_quizzes:
        existing_q = db.session.get(MissionQuiz, q.id)
        if not existing_q:
            db.session.add(q)
        else:
            existing_q.question = q.question
            existing_q.answer = q.answer
            existing_q.explanation = q.explanation
            existing_q.xp_reward = q.xp_reward
    db.session.commit()

    # ── Hints (1 per Mission) ──────────────────────────────────────────────
    hints_data = [
        ('h_l7_1', 'lab7_m1', 'Look at the IoT Gateway Telemetry inspector. Notice how 184 devices report identical metrics across different locations, indicating lack of natural variation.'),
        ('h_l7_2', 'lab7_m2', 'Inspect the Web3 Oracle feed NOVA-PRICE-ORACLE. Check how external telemetry aggregation ingested the gateway stream directly into smart contract pricing.'),
        ('h_l7_3', 'lab7_m3', 'Audit MODEL-ORION training logs. Find how historical synthetic telemetry was injected into training feedback, causing the AI to classify anomalies as normal.'),
        ('h_l7_4', 'lab7_m4', 'Review the 21-Node Validator Grid. Observe the 3:2 consensus split caused by conflicting oracle ingestion paths while AI suppressed circuit breakers.'),
        ('h_l7_5', 'lab7_m5', 'Reconstruct the complete cross-layer trust chain: IoT Sensor -> Telemetry Gateway -> Web3 Oracle -> AI Sentinel -> Blockchain State -> Consensus Split.'),
    ]

    for i, (h_id, m_id, content) in enumerate(hints_data, 1):
        h = db.session.get(Hint, h_id)
        if not h:
            h = Hint(id=h_id, mission_id=m_id, hint_text=content, xp_cost=0, sort_order=i)
            db.session.add(h)
        else:
            h.hint_text = content
            h.xp_cost = 0
            h.sort_order = i
    db.session.commit()

    # ── Evidence Items (5 Forensic Artifacts) ──────────────────────────────
    evidence_data = [
        ('IOT-E11', 'lab7', 'Synchronized IoT Telemetry Log', 'Forensic capture from GATEWAY-GW-184 showing artificial synchronization across 184 geographically dispersed physical sensors.'),
        ('ORACLE-E12', 'lab7', 'Aggregated Oracle Data Feed', 'Raw payload from NOVA-PRICE-ORACLE showing how corrupted IoT telemetry was ingested directly into on-chain price state.'),
        ('AI-E13', 'lab7', 'Poisoned AI Training Feedback', 'Training audit log for MODEL-ORION revealing synthetic device events embedded as legitimate ground truth (EMB-IOT-9041).'),
        ('CONSENSUS-E14', 'lab7', 'Validator State Root Divergence Trace', 'Consensus telemetry showing 3:2 validator partition between proposing node VALIDATOR-V03 and dissenting node VALIDATOR-V05.'),
        ('GOV-E15', 'lab7', 'Unified Cross-Layer Containment Proposal', 'Emergency governance execution (GOV-NEX-071) isolating compromised gateway, flushing poisoned AI weights, and restoring unified consensus.'),
    ]

    for ev_id, l_id, title, desc in evidence_data:
        ev = db.session.get(Evidence, ev_id)
        if not ev:
            ev = Evidence(id=ev_id, lab_id=l_id, name=title, description=desc)
            db.session.add(ev)
        else:
            ev.name = title
            ev.description = desc
    db.session.commit()

    # ── Flags (Master Case Flag) ───────────────────────────────────────────
    flag_val = 'NEXORA{v4n1sh1ng_c0ns3nsus_n3x071}'
    existing_flag = Flag.query.filter_by(lab_id='lab7').first()
    if not existing_flag:
        flag = Flag(id='f7', lab_id='lab7', flag_value=flag_val)
        db.session.add(flag)
    else:
        existing_flag.flag_value = flag_val
    db.session.commit()

    print("Seeded PRO Lab 02: THE VANISHING CONSENSUS (lab7) with 30 hands-on questions covering IoT x AI x Web3 x Blockchain.")


if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_vanishing_consensus()
