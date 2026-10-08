from extensions import db
from sqlalchemy import text

def get_leaderboard(limit=50):
    """Returns leaderboard statistics."""
    query = text('''
        SELECT 
            u.username,
            (
                COALESCE((SELECT SUM(score) FROM lab_progress lp WHERE lp.user_id = u.id), 0) +
                COALESCE((SELECT SUM(score) FROM manual_lab_progress mlp WHERE mlp.user_id = u.id), 0) +
                COALESCE((SELECT SUM(c.points) FROM challenge_progress cp JOIN challenges c ON cp.challenge_id = c.id WHERE cp.user_id = u.id), 0) +
                COALESCE((SELECT SUM(lsp.score) FROM lab_session_progress lsp
                          JOIN lab_sessions ls ON lsp.session_id = ls.id
                          WHERE ls.user_id = u.id), 0)
            ) as total_xp,
            (
                COALESCE((SELECT COUNT(*) FROM lab_progress lp WHERE lp.user_id = u.id AND lp.status = 'COMPLETED'), 0) +
                COALESCE((SELECT COUNT(*) FROM manual_lab_progress mlp WHERE mlp.user_id = u.id AND mlp.status = 'COMPLETED'), 0) +
                COALESCE((SELECT COUNT(*) FROM lab_sessions ls WHERE ls.user_id = u.id AND ls.status = 'COMPLETED'), 0)
            ) as labs_completed,
            (
                COALESCE((SELECT COUNT(*) FROM mission_progress mp WHERE mp.user_id = u.id AND mp.status = 'COMPLETED'), 0) +
                COALESCE((SELECT COUNT(*) FROM lab_session_mission_progress lsmp
                          JOIN lab_sessions ls2 ON lsmp.session_id = ls2.id
                          WHERE ls2.user_id = u.id AND lsmp.status = 'COMPLETED'), 0)
            ) as missions_completed
        FROM users u
        WHERE u.role = 'student'
        ORDER BY total_xp DESC, labs_completed DESC
        LIMIT :limit
    ''')
    result = db.session.execute(query, {'limit': limit}).fetchall()
    
    # Convert Row objects to dict-like objects for the template
    return [
        {
            'username': row.username,
            'total_xp': row.total_xp,
            'labs_completed': row.labs_completed,
            'missions_completed': row.missions_completed
        }
        for row in result
    ]
