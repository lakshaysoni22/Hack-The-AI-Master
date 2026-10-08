import os
import pytest
import sqlite3
import tempfile
from app import app, init_db, limiter
from services.progress_service import initialize_user_progress

@pytest.fixture
def client():
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    os.environ['DATABASE_PATH'] = db_path
    import app as main_app
    main_app.DATABASE = db_path
    
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False 
    app.config['RATELIMIT_ENABLED'] = False
    limiter.enabled = False
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize schema
            db = sqlite3.connect(db_path)
            db.row_factory = sqlite3.Row
            with app.open_resource('database/schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            
            # Seed basic data
            c = db.cursor()
            c.execute("INSERT INTO labs (id, name, topic, difficulty, description) VALUES ('lab1', 'L1', 'T1', 'B', 'D1')")
            c.execute("INSERT INTO labs (id, name, topic, difficulty, description) VALUES ('lab2', 'L2', 'T2', 'B', 'D2')")
            c.execute("INSERT INTO labs (id, name, topic, difficulty, description) VALUES ('lab4', 'L4', 'T4', 'B', 'D4')")
            c.execute("INSERT INTO missions (id, lab_id, mission_number, title, description) VALUES ('lab1_m1', 'lab1', 1, 'M1', 'D1')")
            c.execute("INSERT INTO missions (id, lab_id, mission_number, title, description) VALUES ('lab2_m1', 'lab2', 1, 'M1', 'D1')")
            c.execute("INSERT INTO missions (id, lab_id, mission_number, title, description) VALUES ('lab4_m1', 'lab4', 1, 'M1', 'D1')")
            
            c.execute("INSERT INTO mission_quiz (id, mission_id, question, answer, explanation, xp_reward) VALUES ('q1', 'lab4_m1', 'Q', 'browser', 'E', 150)")
            c.execute("INSERT INTO hints (id, mission_id, hint_text, xp_cost, sort_order) VALUES ('h1', 'lab1_m1', 'Network tab', 10, 1)")
            c.execute("INSERT INTO hints (id, mission_id, hint_text, xp_cost, sort_order) VALUES ('h2', 'lab1_m1', 'X-Custom-Flag', 20, 2)")
            db.commit()
            db.close()
            
        yield client
        
    os.close(db_fd)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass # Windows SQLite file locking issue

@pytest.fixture
def auth_client(client):
    """Registers and logs in a test user, returning the client and user_id"""
    import uuid
    uname = f'testuser_{uuid.uuid4().hex[:8]}'
    response = client.post('/register', data={
        'username': uname,
        'password': 'testpassword'
    })
    
    assert response.status_code == 302, f"Registration failed: {response.data.decode('utf-8')}"
    
    # We can get user_id from session context
    with client.session_transaction() as sess:
        user_id = sess['user_id']
        
    return client, user_id
