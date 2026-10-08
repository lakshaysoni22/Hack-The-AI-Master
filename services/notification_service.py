import os
import smtplib
import threading
from email.message import EmailMessage
from models import User
from extensions import db
from app import app

def send_email_async(app_context, subject, body, recipients):
    """Sends an email asynchronously so it doesn't block the request."""
    with app_context:
        # Get SMTP settings from env (or use defaults for testing)
        smtp_host = os.environ.get('SMTP_HOST', 'localhost')
        smtp_port = int(os.environ.get('SMTP_PORT', 1025))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASS')
        
        for email in recipients:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@hacktheai.com')
            msg['To'] = email

            try:
                if smtp_host == 'localhost' or not smtp_user:
                    print(f"--- MOCK EMAIL ---")
                    print(f"To: {email}\nSubject: {subject}\n{body}")
                    print(f"------------------")
                else:
                    with smtplib.SMTP(smtp_host, smtp_port) as server:
                        if smtp_user and smtp_pass:
                            server.starttls()
                            server.login(smtp_user, smtp_pass)
                        server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

def notify_all_users_new_lab(lab_name, lab_topic):
    """Fetches all student emails and sends them a notification about the new lab."""
    # We must use app_context for the background thread to use the DB
    app_context = app.app_context()
    
    # Get all users who have an email
    users = User.query.filter(User.role == 'student', User.email.isnot(None)).all()
    recipients = [user.email for user in users]
    
    if not recipients:
        print("No users with email addresses found.")
        return

    subject = f"New Lab Available: {lab_name}"
    body = f"Hello Hacker,\n\nA new lab has been added to HackTheAI!\n\nName: {lab_name}\nTopic: {lab_topic}\n\nLog in now to test your skills!"
    
    # Start thread
    thread = threading.Thread(target=send_email_async, args=(app_context, subject, body, recipients))
    thread.daemon = True
    thread.start()
