from extensions import db
from models import Lab, Mission, LabProgress, MissionProgress

def initialize_user_progress(user_id):
    """
    Discovers all active labs and creates progress rows.
    Implements standard unlocking rule: Lab 1 AVAILABLE, others LOCKED initially.
    """
    labs = Lab.query.order_by(Lab.id.asc()).all()
    
    # Lab unlock logic:
    # Lab 1 is always available for a new user.
    # Other labs are locked initially.
    for i, lab in enumerate(labs):
        lab_id = lab.id
        status = 'AVAILABLE' if i == 0 else 'LOCKED'
        
        # Insert lab progress if it doesn't exist
        existing_lp = LabProgress.query.filter_by(user_id=user_id, lab_id=lab_id).first()
        if not existing_lp:
            lp = LabProgress(user_id=user_id, lab_id=lab_id, status=status)
            db.session.add(lp)
        
        # Initialize mission progress for this lab
        missions = Mission.query.filter_by(lab_id=lab_id).order_by(Mission.mission_number.asc()).all()
        for j, mission in enumerate(missions):
            mission_id = mission.id
            # Only the first mission is available IF the lab is available, else locked
            m_status = 'AVAILABLE' if (i == 0 and j == 0) else 'LOCKED'
            
            existing_mp = MissionProgress.query.filter_by(user_id=user_id, mission_id=mission_id).first()
            if not existing_mp:
                mp = MissionProgress(user_id=user_id, lab_id=lab_id, mission_id=mission_id, status=m_status)
                db.session.add(mp)
                
    # Caller should commit

def update_unlocks(user_id):
    """
    Evaluates progression rules:
    1. Inside each lab: if Mission N is COMPLETED, Mission N+1 becomes AVAILABLE (if LOCKED).
    2. If all missions in Lab N are COMPLETED, Lab N becomes COMPLETED.
    3. If Lab N is COMPLETED, Lab N+1 becomes AVAILABLE (and its first mission becomes AVAILABLE).
    """
    labs = Lab.query.order_by(Lab.id.asc()).all()
    
    # 1. Intra-lab mission progression
    for lab in labs:
        missions = Mission.query.filter_by(lab_id=lab.id).order_by(Mission.mission_number.asc()).all()
        for idx in range(len(missions) - 1):
            curr_m = missions[idx]
            next_m = missions[idx + 1]
            
            curr_mp = MissionProgress.query.filter_by(user_id=user_id, mission_id=curr_m.id).first()
            if curr_mp and curr_mp.status == 'COMPLETED':
                next_mp = MissionProgress.query.filter_by(user_id=user_id, mission_id=next_m.id).first()
                if not next_mp:
                    next_mp = MissionProgress(user_id=user_id, lab_id=lab.id, mission_id=next_m.id, status='AVAILABLE')
                    db.session.add(next_mp)
                elif next_mp.status == 'LOCKED':
                    next_mp.status = 'AVAILABLE'
                    db.session.add(next_mp)

    # 2. Inter-lab progression
    for i in range(len(labs) - 1):
        current_lab = labs[i].id
        next_lab = labs[i+1].id
        
        curr_progress = LabProgress.query.filter_by(user_id=user_id, lab_id=current_lab).first()
        next_progress = LabProgress.query.filter_by(user_id=user_id, lab_id=next_lab).first()
        
        if curr_progress and curr_progress.status == 'COMPLETED':
            if not next_progress:
                next_progress = LabProgress(user_id=user_id, lab_id=next_lab, status='AVAILABLE')
                db.session.add(next_progress)
            elif next_progress.status == 'LOCKED':
                next_progress.status = 'AVAILABLE'
                db.session.add(next_progress)
                
            # Unlock first mission of next lab
            first_mission = Mission.query.filter_by(lab_id=next_lab).order_by(Mission.mission_number.asc()).first()
            if first_mission:
                fm_progress = MissionProgress.query.filter_by(user_id=user_id, mission_id=first_mission.id).first()
                if not fm_progress:
                    fm_progress = MissionProgress(user_id=user_id, lab_id=next_lab, mission_id=first_mission.id, status='AVAILABLE')
                    db.session.add(fm_progress)
                elif fm_progress.status == 'LOCKED':
                    fm_progress.status = 'AVAILABLE'
                    db.session.add(fm_progress)
    # Caller should commit
