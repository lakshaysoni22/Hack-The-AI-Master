from flask import Blueprint, render_template, request, redirect, url_for, session, g
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from services.progress_service import initialize_user_progress
from services.audit_service import log_action
from services.user_service import get_user_by_username, create_user
from extensions import limiter, db
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    # Add more complexity rules if requested later
    return True, ""

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            log_action(user.id, 'LOGIN_SUCCESS')
            return redirect(url_for('dashboard.dashboard'))
        if user:
            log_action(user.id, 'LOGIN_FAILED')
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if get_user_by_username(username):
            return render_template('register.html', error="Username taken.")

        
        valid, msg = is_valid_password(password)
        if not valid:
            return render_template('register.html', error=msg)

        try:
            hashed_password = generate_password_hash(password)
            user_id = create_user(username, hashed_password, email)
            # Initialize progress using the centralized service
            initialize_user_progress(user_id)

            db.session.commit()
            session['user_id'] = user_id
            session['username'] = username
            log_action(user_id, 'REGISTER')
            return redirect(url_for('dashboard.dashboard'))
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error="Username taken.")
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        log_action(session['user_id'], 'LOGOUT')
    session.pop('user_id', None)
    return redirect(url_for('index'))
