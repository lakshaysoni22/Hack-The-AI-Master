from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from models import LabProgress, Lab

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    
    # Get overall stats
    progress_rows = LabProgress.query.filter_by(user_id=user_id).all()
    
    total_labs = 5
    completed = sum(1 for row in progress_rows if row.status == 'COMPLETED')
    
    # Get recent labs
    labs = db.session.query(
        Lab.id, Lab.name, Lab.topic, LabProgress.status
    ).outerjoin(
        LabProgress, (Lab.id == LabProgress.lab_id) & (LabProgress.user_id == user_id)
    ).order_by(Lab.id.asc()).all()
    
    # Convert tuples to dict-like objects for template
    labs_list = [{'id': l.id, 'name': l.name, 'topic': l.topic, 'status': l.status} for l in labs]
    
    return render_template('dashboard.html', completed=completed, total_labs=total_labs, labs=labs_list)
