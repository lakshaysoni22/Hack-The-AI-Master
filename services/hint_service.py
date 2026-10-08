from extensions import db
from models import Hint, HintUsage, LabProgress

def get_hint(user_id, lab_id, mission_id):
    """
    Retrieves the next available hint for a mission, deducting XP.
    Returns (success, message, hint_text)
    """
    # Get all hints for this mission ordered by sort_order
    hints = Hint.query.filter_by(mission_id=mission_id).order_by(Hint.sort_order.asc()).all()
    if not hints:
        return False, "No hints available for this mission.", None
        
    # Find the next unused hint
    for hint in hints:
        usage = HintUsage.query.filter_by(user_id=user_id, hint_id=hint.id).first()
        if not usage:
            # We found the next hint. Check XP
            lp = LabProgress.query.filter_by(user_id=user_id, lab_id=lab_id).first()
            cost = hint.xp_cost
            if hint.sort_order == 1:
                cost = 0  # First hint is always free
            if not lp:
                lp = LabProgress(user_id=user_id, lab_id=lab_id, score=0)
                db.session.add(lp)
                
            if lp.score < cost:
                return False, f"Not enough XP. Need {cost} XP.", None
                
            # Deduct XP and record usage
            lp.score = max(0, lp.score - cost)
            db.session.add(lp)
            
            new_usage = HintUsage(user_id=user_id, hint_id=hint.id)
            db.session.add(new_usage)
            db.session.commit()
            
            return True, "Hint unlocked.", hint.hint_text
            
    return False, "You have unlocked all hints for this mission.", None
