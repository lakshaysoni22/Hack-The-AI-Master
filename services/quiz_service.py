from extensions import db
from models import MissionQuiz, QuizAttempt, MissionProgress, LabProgress, Mission, EvidenceProgress

def evaluate_quiz(user_id, lab_id, mission_id, answer, question_id=None):
    """
    Evaluates a quiz answer against the database.
    Supports individual sub-questions (25 questions total across 5 chapters).
    Returns (success, message, xp_awarded, extra_data)
    """
    # Find the target quiz
    if question_id:
        quiz = MissionQuiz.query.filter_by(id=question_id).first()
    else:
        # Fallback to first uncompleted or first quiz for this mission
        quizzes = MissionQuiz.query.filter_by(mission_id=mission_id).order_by(MissionQuiz.id.asc()).all()
        quiz = quizzes[0] if quizzes else None

    if not quiz:
        return False, "No quiz found for this mission.", 0, {}

    user_raw = answer.strip().lower()
    target_raw = quiz.answer.strip().lower()

    user_clean = user_raw.replace('%', '').replace('_', ' ').replace('-', ' ').strip()
    target_clean = target_raw.replace('%', '').replace('_', ' ').replace('-', ' ').strip()

    user_nospace = ''.join(c for c in user_clean if c.isalnum())
    target_nospace = ''.join(c for c in target_clean if c.isalnum())

    correct = (
        (user_clean == target_clean) or 
        (user_raw == target_raw) or 
        (bool(user_nospace) and user_nospace == target_nospace)
    )
    
    # Context-aware flexible fuzzy matching
    if not correct:
        if 'modify' in target_clean and 'wallet' in target_clean and ('modify' in user_clean and 'wallet' in user_clean):
            correct = True
        elif target_clean == 'unknown' and 'unknown' in user_clean:
            correct = True
        elif target_clean in ['95', '95%'] and ('95' in user_clean):
            correct = True
        elif 'orion' in target_clean and 'nexus' in target_clean and ('orion' in user_clean and 'nexus' in user_clean):
            correct = True
        elif 'nif' in target_clean and '2038' in target_clean and ('nif' in user_clean and '2038' in user_clean):
            correct = True
        elif '82400' in target_clean and ('82400' in user_clean or '82,400' in user_clean):
            correct = True
        elif 'bridge' in target_clean and 'core' in target_clean and ('bridge' in user_clean and 'core' in user_clean and '04' in user_clean):
            correct = True
        elif 'adv' in target_clean and 'convergence' in target_clean and ('convergence' in user_clean or 'adv' in user_clean):
            correct = True
        elif 'human' in target_clean and 'approval' in target_clean and ('human' in user_clean or 'multisig' in user_clean or 'multi sig' in user_clean):
            correct = True
        elif 'nex' in target_clean and 'sess' in target_clean and ('994' in user_clean):
            correct = True
        elif '0x9f4a1c78' in target_clean and ('9f4a1c78' in user_clean):
            correct = True
        elif 'pol' in target_clean and 'settle' in target_clean and ('settle' in user_clean or 'treasury' in user_clean):
            correct = True
        elif 'automated' in target_clean and 'signer' in target_clean and ('signer' in user_clean or 'broker' in user_clean):
            correct = True
        elif 'liquidity' in target_clean and 'pool' in target_clean and ('liquidity' in user_clean or 'pool' in user_clean):
            correct = True
        elif 'oracle' in target_clean and 'poison' in target_clean and ('oracle' in user_clean or 'poison' in user_clean):
            correct = True
        elif 'relayer' in target_clean and '09' in target_clean and ('relayer' in user_clean and '09' in user_clean):
            correct = True
        elif 'legitimate' in target_clean and 'inflow' in target_clean and ('inflow' in user_clean or 'legitimate' in user_clean):
            correct = True
        elif 'validator' in target_clean and 'v05' in target_clean and ('v05' in user_clean or 'validator' in user_clean):
            correct = True
        elif 'validator' in target_clean and 'v03' in target_clean and ('v03' in user_clean or 'validator' in user_clean):
            correct = True
        elif 'emb' in target_clean and '9041' in target_clean and ('9041' in user_clean):
            correct = True
        elif 'gov' in target_clean and '071' in target_clean and ('gov' in user_clean and '071' in user_clean):
            correct = True
        elif '4820' in target_clean and ('4820' in user_clean or '4,820' in user_clean):
            correct = True
        elif '142' in target_clean and ('142' in user_clean or '142.10' in user_clean):
            correct = True
        elif '2500000' in target_clean and ('2500000' in user_clean or '2.5m' in user_clean or '2,500,000' in user_clean):
            correct = True
        elif '0x4f8e' in target_clean and ('4f8e' in user_clean):
            correct = True
        elif '0x98a2' in target_clean and ('98a2' in user_clean):
            correct = True
        elif 'bft' in target_clean and ('bft' in user_clean or 'pos' in user_clean):
            correct = True
        # Lab 2: IoT x Web3 x AI x Blockchain flexible matching
        elif 'variation' in target_clean and ('variation' in user_clean or 'entropy' in user_clean or 'jitter' in user_clean or 'natural' in user_clean):
            correct = True
        elif 'environmental' in target_clean and ('condition' in user_clean or 'environment' in user_clean or 'different' in user_clean or 'location' in user_clean):
            correct = True
        elif 'device' in target_clean and 'telemetry' in target_clean and ('device' in user_clean or 'flash' in user_clean or 'local' in user_clean):
            correct = True
        elif 'gateway' in target_clean and 'manipulate' in target_clean and ('gateway' in user_clean or 'upstream' in user_clean or 'manipulat' in user_clean):
            correct = True
        elif 'sequence' in target_clean and ('sequence' in user_clean or 'log' in user_clean or 'order' in user_clean or 'history' in user_clean):
            correct = True
        elif 'ingestion' in target_clean and ('ingestion' in user_clean or 'telemetry' in user_clean or 'data layer' in user_clean or 'aggregation' in user_clean):
            correct = True
        elif 'external' in target_clean and 'aggregation' in target_clean and ('aggregation' in user_clean or 'telemetry' in user_clean or 'gateway' in user_clean or 'external' in user_clean):
            correct = True
        elif 'oracle' in target_clean and 'truth' in target_clean and ('truth' in user_clean or 'oracle' in user_clean or 'external' in user_clean or 'feed' in user_clean):
            correct = True
        elif 'upstream' in target_clean and 'stream' in target_clean and ('stream' in user_clean or 'source' in user_clean or 'same' in user_clean or 'iot' in user_clean):
            correct = True
        elif 'poison' in target_clean and 'aggregate' in target_clean and ('aggregate' in user_clean or 'trusted' in user_clean or 'state' in user_clean or 'poison' in user_clean):
            correct = True
        elif 'corrupted' in target_clean and 'source' in target_clean and ('source' in user_clean or 'common' in user_clean or 'corrupt' in user_clean or 'repeat' in user_clean):
            correct = True
        elif 'trusted' in target_clean and 'external' in target_clean and ('oracle' in user_clean or 'trusted' in user_clean or 'boundary' in user_clean or 'external' in user_clean):
            correct = True
        elif 'synchronized' in target_clean and 'iot' in target_clean and ('synchronized' in user_clean or 'sync' in user_clean or 'telemetry' in user_clean):
            correct = True
        elif 'synthetic' in target_clean and 'injection' in target_clean and ('synthetic' in user_clean or 'injection' in user_clean or 'artificial' in user_clean):
            correct = True
        elif 'malicious' in target_clean and 'normal' in target_clean and ('normal' in user_clean or 'malicious' in user_clean or 'blind' in user_clean or 'suppress' in user_clean):
            correct = True
        elif 'feature' in target_clean and 'input' in target_clean and ('feature' in user_clean or 'input' in user_clean or 'feed' in user_clean or 'sensor' in user_clean):
            correct = True
        elif 'trained' in target_clean and 'poison' in target_clean and ('train' in user_clean or 'poison' in user_clean or 'dataset' in user_clean or 'weight' in user_clean):
            correct = True
        elif 'legitimate' in target_clean and 'learned' in target_clean and ('legitimate' in user_clean or 'baseline' in user_clean or 'learn' in user_clean or 'pattern' in user_clean or 'no' in user_clean):
            correct = True
        elif 'altering' in target_clean and 'smart' in target_clean and ('smart contract' in user_clean or 'oracle' in user_clean or 'input' in user_clean or 'execution' in user_clean):
            correct = True
        elif 'timing' in target_clean and 'paths' in target_clean and ('timing' in user_clean or 'path' in user_clean or 'latency' in user_clean or 'conflict' in user_clean):
            correct = True
        elif 'suppressed' in target_clean and 'warning' in target_clean and ('suppress' in user_clean or 'warning' in user_clean or 'alarm' in user_clean or 'normal' in user_clean or 'circuit' in user_clean):
            correct = True
        elif 'deterministically' in target_clean and ('deterministic' in user_clean or 'local' in user_clean or 'protocol' in user_clean or 'valid' in user_clean):
            correct = True
        elif 'iot' in target_clean and 'oracle' in target_clean and 'blockchain' in target_clean and ('iot' in user_clean and ('blockchain' in user_clean or 'ai' in user_clean or 'web3' in user_clean or 'oracle' in user_clean)):
            correct = True
        elif 'boundaries' in target_clean and 'exploited' in target_clean and ('boundary' in user_clean or 'trust' in user_clean or 'healthy' in user_clean or 'cross' in user_clean):
            correct = True
        elif 'cross' in target_clean and 'trust' in target_clean and ('trust' in user_clean or 'layer' in user_clean or 'cross' in user_clean or 'depend' in user_clean):
            correct = True

            
    # Record attempt using quiz.id as identifier in the attempt log
    attempt = QuizAttempt(user_id=user_id, mission_id=quiz.id, answer=answer, correct=correct)
    db.session.add(attempt)
    
    if not correct:
        db.session.commit()
        # Helpful guidance
        if '0x7c41' in user_clean:
            return False, "Target address detected! The question is asking for the on-chain status (e.g. UNKNOWN).", 0, {'quiz_id': quiz.id}
        if 'orion-dec' in user_clean and 'nif' not in user_clean:
            return False, "That's the decision ID! What was the specific intelligence reference code (starts with NIF-)?", 0, {'quiz_id': quiz.id}
        if 'intel-ingestor' in user_clean and 'modify' not in user_clean:
            return False, "That's the microservice name! What unauthorized permission was assigned to it?", 0, {'quiz_id': quiz.id}
        return False, "Incorrect finding. Inspect the investigator clues in Terminal or DevTools and try again.", 0, {'quiz_id': quiz.id}
    
    # Award XP for this specific question
    xp = quiz.xp_reward or 50
    lab_prog = LabProgress.query.filter_by(user_id=user_id, lab_id=lab_id).first()
    if lab_prog:
        lab_prog.score = (lab_prog.score or 0) + xp
        db.session.add(lab_prog)

    # Check how many quizzes exist for this mission and how many user has completed
    all_mission_quizzes = MissionQuiz.query.filter_by(mission_id=mission_id).order_by(MissionQuiz.id.asc()).all()
    quiz_ids = [q.id for q in all_mission_quizzes]
    
    solved_quiz_ids = {
        qa.mission_id for qa in QuizAttempt.query.filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.mission_id.in_(quiz_ids),
            QuizAttempt.correct == True
        ).all()
    }
    solved_quiz_ids.add(quiz.id)

    mission_completed = len(solved_quiz_ids) >= len(all_mission_quizzes)
    
    if mission_completed:
        mission_prog = MissionProgress.query.filter_by(user_id=user_id, mission_id=mission_id).first()
        if not mission_prog:
            mission_prog = MissionProgress(user_id=user_id, lab_id=lab_id, mission_id=mission_id, status='COMPLETED')
        else:
            mission_prog.status = 'COMPLETED'
        db.session.add(mission_prog)

        # Unlock next mission
        _unlock_next_mission(user_id, lab_id, mission_id)

        # Auto-collect cryptographic evidence
        _collect_evidence_for_mission(user_id, lab_id, mission_id)
            
        db.session.commit()
        return True, f"🎉 All {len(all_mission_quizzes)} investigation objectives verified for this chapter! Evidence secured.", xp, {
            'quiz_id': quiz.id,
            'mission_completed': True,
            'solved_count': len(solved_quiz_ids),
            'total_count': len(all_mission_quizzes),
            'explanation': quiz.explanation
        }
    
    db.session.commit()
    return True, f"✓ Objective verified! ({len(solved_quiz_ids)}/{len(all_mission_quizzes)} complete)", xp, {
        'quiz_id': quiz.id,
        'mission_completed': False,
        'solved_count': len(solved_quiz_ids),
        'total_count': len(all_mission_quizzes),
        'explanation': quiz.explanation
    }


def _unlock_next_mission(user_id, lab_id, mission_id):
    """Unlocks the next sequential mission in the lab."""
    current_mission = Mission.query.get(mission_id)
    if not current_mission:
        return
    next_m = Mission.query.filter_by(
        lab_id=lab_id,
        mission_number=current_mission.mission_number + 1
    ).first()
    if next_m:
        next_mp = MissionProgress.query.filter_by(user_id=user_id, mission_id=next_m.id).first()
        if not next_mp:
            next_mp = MissionProgress(user_id=user_id, lab_id=lab_id, mission_id=next_m.id, status='AVAILABLE')
            db.session.add(next_mp)
        elif next_mp.status == 'LOCKED':
            next_mp.status = 'AVAILABLE'
            db.session.add(next_mp)


def _collect_evidence_for_mission(user_id, lab_id, mission_id):
    """Auto-collects cryptographic evidence for lab6 and lab7 chapters."""
    evidence_map = {
        'lab6_m1': 'e_l6_01',
        'lab6_m2': 'e_l6_02',
        'lab6_m3': 'e_l6_03',
        'lab6_m4': 'e_l6_04',
        'lab6_m5': 'e_l6_05',
        'lab7_m1': 'e_l7_01',
        'lab7_m2': 'e_l7_02',
        'lab7_m3': 'e_l7_03',
        'lab7_m4': 'e_l7_04',
        'lab7_m5': 'e_l7_05',
    }
    ev_id = evidence_map.get(mission_id)
    if ev_id:
        ep = EvidenceProgress.query.filter_by(user_id=user_id, evidence_id=ev_id).first()
        if not ep:
            ep = EvidenceProgress(user_id=user_id, evidence_id=ev_id, collected=True)
            db.session.add(ep)
        elif not ep.collected:
            ep.collected = True
            db.session.add(ep)

