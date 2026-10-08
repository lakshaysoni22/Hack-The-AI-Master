from extensions import db
from models import AuditLog

def log_action(user_id, action, details=None):
    log = AuditLog(user_id=user_id, action=action, details=details)
    db.session.add(log)
    # Note: we generally commit in the route or let it flush, but for audit we can commit
    db.session.commit()
