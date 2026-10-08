from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='student')
    
    # Relationships
    lab_progress = db.relationship('LabProgress', backref='user', lazy=True)
    mission_progress = db.relationship('MissionProgress', backref='user', lazy=True)
    evidence_progress = db.relationship('EvidenceProgress', backref='user', lazy=True)
    manual_lab_progress = db.relationship('ManualLabProgress', backref='user', lazy=True)
    challenge_progress = db.relationship('ChallengeProgress', backref='user', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)
class Lab(db.Model):
    __tablename__ = 'labs'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    
    # Relationships
    missions = db.relationship('Mission', backref='lab', lazy=True)
    flags = db.relationship('Flag', backref='lab', lazy=True)
    evidence = db.relationship('Evidence', backref='lab', lazy=True)
    progress = db.relationship('LabProgress', backref='lab', lazy=True)

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.String(50), primary_key=True)
    lab_id = db.Column(db.String(50), db.ForeignKey('labs.id'), nullable=False)
    mission_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Relationships
    progress = db.relationship('MissionProgress', backref='mission', lazy=True)

class MissionProgress(db.Model):
    __tablename__ = 'mission_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lab_id = db.Column(db.String(50), db.ForeignKey('labs.id'), nullable=False)
    mission_id = db.Column(db.String(50), db.ForeignKey('missions.id'), nullable=False)
    status = db.Column(db.String(50), default='LOCKED') # LOCKED, AVAILABLE, IN PROGRESS, COMPLETED
    completed_at = db.Column(db.DateTime, nullable=True)

class MissionQuiz(db.Model):
    __tablename__ = 'mission_quiz'
    id = db.Column(db.String(50), primary_key=True)
    mission_id = db.Column(db.String(50), db.ForeignKey('missions.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    xp_reward = db.Column(db.Integer, default=150)

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mission_id = db.Column(db.String(50), db.ForeignKey('missions.id'), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Hint(db.Model):
    __tablename__ = 'hints'
    id = db.Column(db.String(50), primary_key=True)
    mission_id = db.Column(db.String(50), db.ForeignKey('missions.id'), nullable=False)
    hint_text = db.Column(db.Text, nullable=False)
    xp_cost = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=1)

class HintUsage(db.Model):
    __tablename__ = 'hint_usage'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hint_id = db.Column(db.String(50), db.ForeignKey('hints.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class LabProgress(db.Model):
    __tablename__ = 'lab_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lab_id = db.Column(db.String(50), db.ForeignKey('labs.id'), nullable=False)
    status = db.Column(db.String(50), default='IN PROGRESS') # IN PROGRESS, COMPLETED
    score = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

class Evidence(db.Model):
    __tablename__ = 'evidence'
    id = db.Column(db.String(50), primary_key=True)
    lab_id = db.Column(db.String(50), db.ForeignKey('labs.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class EvidenceProgress(db.Model):
    __tablename__ = 'evidence_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evidence_id = db.Column(db.String(50), db.ForeignKey('evidence.id'), nullable=False)
    collected = db.Column(db.Boolean, default=False)
    collected_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Flag(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.String(50), primary_key=True)
    lab_id = db.Column(db.String(50), db.ForeignKey('labs.id'), nullable=False)
    flag_value = db.Column(db.String(200), nullable=False)

class ManualLab(db.Model):
    __tablename__ = 'manual_labs'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)

class ManualLabFlag(db.Model):
    __tablename__ = 'manual_lab_flags'
    id = db.Column(db.Integer, primary_key=True)
    manual_lab_id = db.Column(db.String(50), db.ForeignKey('manual_labs.id'), nullable=False)
    flag_value = db.Column(db.String(200), nullable=False)

class ManualLabProgress(db.Model):
    __tablename__ = 'manual_lab_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manual_lab_id = db.Column(db.String(50), db.ForeignKey('manual_labs.id'), nullable=False)
    status = db.Column(db.String(50), default='IN PROGRESS')
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=100)
    flag_value = db.Column(db.String(200), nullable=False)
    
class ChallengeProgress(db.Model):
    __tablename__ = 'challenge_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.String(50), db.ForeignKey('challenges.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# =========================================================================
# ZIP-to-Interactive Lab Engine Models
# =========================================================================

class UploadedLab(db.Model):
    """Stores parsed lab manifest from uploaded ZIP files."""
    __tablename__ = 'uploaded_labs'
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, default='General')
    difficulty = db.Column(db.String(50), nullable=False, default='Beginner')
    concept = db.Column(db.String(200), nullable=True)
    storyline = db.Column(db.Text, nullable=True)            # JSON or markdown storyline text
    description = db.Column(db.Text, nullable=True)           # Short description for catalog
    estimated_time = db.Column(db.Integer, default=30)        # minutes
    total_points = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='draft')        # draft, published, archived
    sort_order = db.Column(db.Integer, nullable=False, default=0)  # learning-path position; labs unlock in this order
    zip_path = db.Column(db.String(500), nullable=True)       # Path to extracted ZIP on disk
    docker_config = db.Column(db.Text, nullable=True)         # JSON: dockerfile path, compose, ports
    target_app_path = db.Column(db.String(500), nullable=True) # Relative path to app dir inside extracted ZIP
    manifest_json = db.Column(db.Text, nullable=True)         # Full normalized manifest as JSON
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    missions = db.relationship('UploadedLabMission', backref='lab', lazy=True, cascade='all, delete-orphan',
                               order_by='UploadedLabMission.mission_number')
    flags = db.relationship('UploadedLabFlag', backref='lab', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('LabSession', backref='lab', lazy=True)


class UploadedLabMission(db.Model):
    """Individual missions within an uploaded lab."""
    __tablename__ = 'uploaded_lab_missions'
    id = db.Column(db.String(80), primary_key=True)
    lab_id = db.Column(db.String(50), db.ForeignKey('uploaded_labs.id'), nullable=False)
    mission_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    objective = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)          # JSON array of instruction steps
    storyline_text = db.Column(db.Text, nullable=True)        # Per-mission storyline continuation
    target_url_path = db.Column(db.String(500), nullable=True) # Relative path in target app
    points = db.Column(db.Integer, default=100)

    # Relationships
    questions = db.relationship('UploadedLabQuestion', backref='mission', lazy=True, cascade='all, delete-orphan',
                                order_by='UploadedLabQuestion.sort_order')
    hints = db.relationship('UploadedLabHint', backref='mission', lazy=True, cascade='all, delete-orphan',
                            order_by='UploadedLabHint.sort_order')


class UploadedLabQuestion(db.Model):
    """Questions attached to a mission, with backend validation config."""
    __tablename__ = 'uploaded_lab_questions'
    id = db.Column(db.String(80), primary_key=True)
    mission_id = db.Column(db.String(80), db.ForeignKey('uploaded_lab_missions.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    validation_type = db.Column(db.String(50), default='ANSWER_MATCH')  # ANSWER_MATCH, REGEX, MULTI_ANSWER
    expected_answer = db.Column(db.Text, nullable=False)      # JSON for multi-answer, string for single
    case_sensitive = db.Column(db.Boolean, default=False)
    explanation = db.Column(db.Text, nullable=True)
    xp_reward = db.Column(db.Integer, default=100)
    sort_order = db.Column(db.Integer, default=1)


class UploadedLabHint(db.Model):
    """Hints for a mission, revealed progressively."""
    __tablename__ = 'uploaded_lab_hints'
    id = db.Column(db.String(80), primary_key=True)
    mission_id = db.Column(db.String(80), db.ForeignKey('uploaded_lab_missions.id'), nullable=False)
    hint_text = db.Column(db.Text, nullable=False)
    xp_cost = db.Column(db.Integer, default=10)
    sort_order = db.Column(db.Integer, default=1)


class UploadedLabFlag(db.Model):
    """Flags for an uploaded lab — server-side only, never sent to frontend."""
    __tablename__ = 'uploaded_lab_flags'
    id = db.Column(db.String(80), primary_key=True)
    lab_id = db.Column(db.String(50), db.ForeignKey('uploaded_labs.id'), nullable=False)
    mission_id = db.Column(db.String(80), nullable=True)      # Optional: tie to specific mission
    flag_value = db.Column(db.String(500), nullable=False)
    flag_description = db.Column(db.String(200), nullable=True)
    points = db.Column(db.Integer, default=100)


class LabSession(db.Model):
    """Active learner lab session with container runtime info."""
    __tablename__ = 'lab_sessions'
    id = db.Column(db.String(80), primary_key=True)           # UUID session ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lab_id = db.Column(db.String(50), db.ForeignKey('uploaded_labs.id'), nullable=False)
    container_id = db.Column(db.String(100), nullable=True)   # Docker container ID
    container_port = db.Column(db.Integer, nullable=True)     # Mapped host port
    status = db.Column(db.String(20), default='STARTING')     # STARTING, ACTIVE, COMPLETED, EXPIRED, ERROR
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    expiration = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    progress = db.relationship('LabSessionProgress', backref='session', lazy=True, uselist=False,
                               cascade='all, delete-orphan')
    mission_progress = db.relationship('LabSessionMissionProgress', backref='session', lazy=True,
                                       cascade='all, delete-orphan')
    question_attempts = db.relationship('LabSessionQuestionAttempt', backref='session', lazy=True,
                                        cascade='all, delete-orphan')
    flag_attempts = db.relationship('LabSessionFlagAttempt', backref='session', lazy=True,
                                    cascade='all, delete-orphan')


class LabSessionProgress(db.Model):
    """Overall progress for a lab session."""
    __tablename__ = 'lab_session_progress'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80), db.ForeignKey('lab_sessions.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_possible = db.Column(db.Integer, default=0)
    missions_completed = db.Column(db.Integer, default=0)
    missions_total = db.Column(db.Integer, default=0)
    hints_used = db.Column(db.Integer, default=0)
    time_spent_seconds = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Integer, default=0)


class LabSessionMissionProgress(db.Model):
    """Per-mission state within a lab session."""
    __tablename__ = 'lab_session_mission_progress'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80), db.ForeignKey('lab_sessions.id'), nullable=False)
    mission_id = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default='LOCKED')       # LOCKED, AVAILABLE, IN_PROGRESS, COMPLETED, FAILED
    score = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)


class LabSessionQuestionAttempt(db.Model):
    """Records each answer attempt for audit and scoring."""
    __tablename__ = 'lab_session_question_attempts'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80), db.ForeignKey('lab_sessions.id'), nullable=False)
    mission_id = db.Column(db.String(80), nullable=False)
    question_id = db.Column(db.String(80), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class LabSessionFlagAttempt(db.Model):
    """Records each flag submission attempt."""
    __tablename__ = 'lab_session_flag_attempts'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80), db.ForeignKey('lab_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lab_id = db.Column(db.String(50), nullable=False)
    mission_id = db.Column(db.String(80), nullable=True)
    flag_submitted = db.Column(db.String(500), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
