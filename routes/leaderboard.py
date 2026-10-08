from flask import Blueprint, render_template, session, redirect, url_for
from services.leaderboard_service import get_leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    leaders = get_leaderboard()
    return render_template('leaderboard.html', title="Leaderboard", leaders=leaders)
