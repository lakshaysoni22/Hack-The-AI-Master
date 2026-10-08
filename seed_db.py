import os
from werkzeug.security import generate_password_hash
from services.progress_service import initialize_user_progress
from extensions import db
from models import (
    User, Lab, Mission, MissionQuiz, Hint, Flag,
    ManualLab, ManualLabFlag
)
from app import app

def seed_database():
    with app.app_context():
        db.create_all()
        # Check if we already have labs
        if Lab.query.first():
            print("Database already seeded.")
            return

        # Create admin user
        admin_pw = generate_password_hash('admin123')
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password=admin_pw, role='admin')
            db.session.add(admin_user)

        hashed_pw = generate_password_hash("password123")
        alex_user = User(username='Alex', password=hashed_pw)
        db.session.add(alex_user)
        db.session.flush() # To get Alex's ID

        # Seed Labs
        labs_data = [
            Lab(id='lab1', name='The Missing Access Control', topic='Authentication vs Authorization', difficulty='Beginner'),
            Lab(id='lab2', name='The Exposed Employee File', topic='Information Disclosure', difficulty='Beginner'),
            Lab(id='lab3', name='The Missing Employee Access', topic='IDOR', difficulty='Beginner'),
            Lab(id='lab4', name='The Tricked Support Ticket', topic='Cross-Site Scripting', difficulty='Beginner -> Pro'),
            Lab(id='lab5', name='The Fake Login Trap', topic='Phishing / Social Engineering', difficulty='Beginner')
        ]
        db.session.add_all(labs_data)
        
        # Seed Missions
        missions_data = [
            Mission(id='lab1_m1', lab_id='lab1', mission_number=1, title='Login to Portal', description='Log in as a standard employee.'),
            Mission(id='lab1_m2', lab_id='lab1', mission_number=2, title='Find Admin Panel', description='Discover the restricted admin functionality.'),
            Mission(id='lab1_m3', lab_id='lab1', mission_number=3, title='Test Authorization', description='Try to access the admin panel.'),
            Mission(id='lab1_m4', lab_id='lab1', mission_number=4, title='Bypass Access Control', description='Exploit improper authorization.'),
            Mission(id='lab1_m5', lab_id='lab1', mission_number=5, title='Identify Fix', description='How to prevent this?'),

            Mission(id='lab2_m1', lab_id='lab2', mission_number=1, title='Explore Web App', description='Look for exposed files.'),
            Mission(id='lab2_m2', lab_id='lab2', mission_number=2, title='Find Backup', description='Locate the backup file.'),
            Mission(id='lab2_m3', lab_id='lab2', mission_number=3, title='Extract Data', description='Extract sensitive information.'),
            Mission(id='lab2_m4', lab_id='lab2', mission_number=4, title='Analyze Impact', description='Explain the impact.'),
            Mission(id='lab2_m5', lab_id='lab2', mission_number=5, title='Secure Config', description='How to secure it?'),

            Mission(id='lab3_m1', lab_id='lab3', mission_number=1, title='View Own Profile', description='Access your own profile data.'),
            Mission(id='lab3_m2', lab_id='lab3', mission_number=2, title='Identify ID', description='Find your object identifier.'),
            Mission(id='lab3_m3', lab_id='lab3', mission_number=3, title='Change ID', description='Try to access another user.'),
            Mission(id='lab3_m4', lab_id='lab3', mission_number=4, title='Extract Peer Data', description='Extract the data.'),
            Mission(id='lab3_m5', lab_id='lab3', mission_number=5, title='Prevent IDOR', description='How to stop IDOR?'),
            
            Mission(id='lab4_m1', lab_id='lab4', mission_number=1, title='Explore Ticket System', description='Find the strange ticket.'),
            Mission(id='lab4_m2', lab_id='lab4', mission_number=2, title='Find Strange Ticket', description='Identify who controls the message.'),
            Mission(id='lab4_m3', lab_id='lab4', mission_number=3, title='Test Input', description='Understand what executes the script.'),
            Mission(id='lab4_m4', lab_id='lab4', mission_number=4, title='Evidence Mode', description='Determine where the XSS executes.'),
            Mission(id='lab4_m5', lab_id='lab4', mission_number=5, title='Fix Ticket System', description='Identify the best defense.'),
            
            Mission(id='lab5_m1', lab_id='lab5', mission_number=1, title='Inspect Message', description='Identify what is suspicious.'),
            Mission(id='lab5_m2', lab_id='lab5', mission_number=2, title='Inspect Link', description='Identify what you should inspect.'),
            Mission(id='lab5_m3', lab_id='lab5', mission_number=3, title='Human Firewall', description='Identify who detects phishing.'),
            Mission(id='lab5_m4', lab_id='lab5', mission_number=4, title='Build Attack Chain', description='Identify what is targeted.'),
            Mission(id='lab5_m5', lab_id='lab5', mission_number=5, title='Stop Attack', description='Identify extra account defense.')
        ]
        db.session.add_all(missions_data)

        # Quizzes
        quizzes = [
            MissionQuiz(id='q_l1_1', mission_id='lab1_m1', question='What type of account did you login as?', answer='employee', explanation='You logged in as a standard employee.', xp_reward=50),
            MissionQuiz(id='q_l1_2', mission_id='lab1_m4', question='What vulnerability allows you to access the admin panel?', answer='idor', explanation='Actually it is broken access control.', xp_reward=100),
            MissionQuiz(id='q_l1_3', mission_id='lab1_m5', question='How do you fix broken access control?', answer='authorization', explanation='Implement proper authorization checks on every endpoint.', xp_reward=150),
            MissionQuiz(id='q_l2_1', mission_id='lab2_m2', question='What extension did the backup file have?', answer='bak', explanation='Backup files often have .bak extensions.', xp_reward=50),
            MissionQuiz(id='q_l2_2', mission_id='lab2_m3', question='What sensitive data was in the file?', answer='passwords', explanation='The file contained plaintext passwords.', xp_reward=100),
            MissionQuiz(id='q_l3_1', mission_id='lab3_m2', question='Where did you find your object identifier?', answer='url', explanation='The ID is passed in the URL parameter.', xp_reward=50),
            MissionQuiz(id='q_l3_2', mission_id='lab3_m5', question='How do you prevent IDOR?', answer='authorization checks', explanation='Always verify the user owns the requested object.', xp_reward=100),
            MissionQuiz(id='q_l4_1', mission_id='lab4_m1', question='What type of payload was submitted in the ticket?', answer='javascript', explanation='The ticket contains an alert(1) payload, which is JavaScript.', xp_reward=100),
            MissionQuiz(id='q_l4_2', mission_id='lab4_m2', question='What vulnerability allows this script to run in the browser?', answer='xss', explanation='Cross-Site Scripting (XSS) allows attackers to inject client-side scripts into web pages viewed by other users.', xp_reward=100),
            MissionQuiz(id='q_l4_3', mission_id='lab4_m3', question='What is the most effective way to prevent XSS?', answer='encoding', explanation='Output encoding neutralizes special characters before rendering them in the browser.', xp_reward=150),
        ]
        db.session.add_all(quizzes)
        
        # Hints
        hints = [
            Hint(id='h_l1_1', mission_id='lab1_m2', hint_text='Look for hidden links in the source code.', xp_cost=10, sort_order=1),
            Hint(id='h_l1_2', mission_id='lab1_m4', hint_text='Try changing your role parameter in the request.', xp_cost=20, sort_order=1),
            Hint(id='h_l4_1', mission_id='lab4_m1', hint_text='Look at the script tags in the ticket body.', xp_cost=10, sort_order=1),
            Hint(id='h_l4_2', mission_id='lab4_m2', hint_text='It stands for Cross-Site Scripting (use acronym).', xp_cost=20, sort_order=1),
            Hint(id='h_l4_3', mission_id='lab4_m3', hint_text='It involves converting characters like < and > into their HTML entities.', xp_cost=30, sort_order=1)
        ]
        db.session.add_all(hints)

        # Initialize progress for the test user
        # Note: We need to flush first so missions are in DB before progress references them
        db.session.flush()
        initialize_user_progress(alex_user.id)

        # Flags
        flags = [
            Flag(id='f1', lab_id='lab1', flag_value='TECHCORP{auth_bypass}'),
            Flag(id='f2', lab_id='lab2', flag_value='TECHCORP{info_leak}'),
            Flag(id='f3', lab_id='lab3', flag_value='TECHCORP{idor_exploited}'),
            Flag(id='f4', lab_id='lab4', flag_value='TECHCORP{xss_ticket_found}'),
            Flag(id='f5', lab_id='lab5', flag_value='TECHCORP{human_firewall}')
        ]
        db.session.add_all(flags)

        # Manual Labs
        manual_labs = [
            ManualLab(id='mlab1', name='Basic Reconnaissance', topic='Network', difficulty='Beginner', target_type='vm'),
            ManualLab(id='mlab2', name='Web App Vulnerability', topic='Web', difficulty='Pro', target_type='container'),
            ManualLab(id='mlab3', name='Active Directory Basics', topic='OSINT', difficulty='Beginner', target_type='web')
        ]
        db.session.add_all(manual_labs)
        
        # Manual Lab Flags
        mlab_flags = [
            ManualLabFlag(id=1, manual_lab_id='mlab1', flag_value='TECHCORP{nmap_recon_master}'),
            ManualLabFlag(id=2, manual_lab_id='mlab2', flag_value='TECHCORP{cmd_injection_win}'),
            ManualLabFlag(id=3, manual_lab_id='mlab3', flag_value='TECHCORP{osint_found}')
        ]
        db.session.add_all(mlab_flags)

        db.session.commit()
        print("Seeded database successfully.")

if __name__ == '__main__':
    seed_database()
