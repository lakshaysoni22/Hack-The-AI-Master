import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from config import get_config
from extensions import csrf, limiter, db, migrate
from flask_talisman import Talisman
from flask_session import Session
import redis
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

load_dotenv()

# Configure basic logging (can be expanded to JSON formatter)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Sentry if DSN is provided
sentry_dsn = os.environ.get("SENTRY_DSN")
if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1,
    )

app = Flask(__name__)
app.config.from_object(get_config())

csrf.init_app(app)
limiter.init_app(app)
logger.info(f"Rate limiter storage backend: {app.config.get('RATELIMIT_STORAGE_URI')}")

# Set up Redis for sessions (Only if REDIS_URL is explicitly provided)
if os.environ.get('REDIS_URL'):
    try:
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_PERMANENT'] = False
        app.config['SESSION_USE_SIGNER'] = True
        redis_url = os.environ.get('REDIS_URL')
        app.config['SESSION_REDIS'] = redis.from_url(redis_url, socket_timeout=2)
        Session(app)
        logger.info("Redis session management initialized.")
    except Exception as e:
        logger.warning(f"Could not connect to Redis for sessions. Falling back to default cookies. Error: {e}")
else:
    logger.info("Using default cookie sessions for local development or serverless deployments.")

# Set up strict security headers
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://fonts.googleapis.com',
        'https://fonts.gstatic.com'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\''
    ],
    'frame-src': [
        '\'self\'',
        'http://localhost:*',
        'http://127.0.0.1:*'
    ]
}
Talisman(
    app,
    content_security_policy=csp,
    force_https=app.config.get('SESSION_COOKIE_SECURE', False),
    # Talisman defaults this to True regardless of our own config, which
    # would force the `Secure` flag onto the session cookie even when
    # nothing in front of this app actually terminates TLS - browsers then
    # silently refuse to store the cookie at all, so every request looks
    # like a fresh, logged-out session. Tie it to the same flag as above.
    session_cookie_secure=app.config.get('SESSION_COOKIE_SECURE', False),
)

db.init_app(app)
import models  # noqa: F401 # Ensure models are loaded before migrate
migrate.init_app(app, db)




from routes.admin import admin_bp
from routes.leaderboard import leaderboard_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.labs import labs_bp
from routes.api import api_bp
from routes.pages import pages_bp


app.register_blueprint(admin_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(labs_bp)
app.register_blueprint(api_bp)
app.register_blueprint(pages_bp)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

from flask_wtf.csrf import CSRFError

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.warning(f"CSRF validation failed: {e.description}")
    return render_template('login.html', error="Your session has expired. Please log in again."), 400

def init_db():
    with app.app_context():
        # create_all safely ignores existing tables
        db.create_all()
        _ensure_uploaded_labs_sort_order_column()
        # Seed only if admin doesn't exist
        if not models.User.query.filter_by(username='admin').first():
            print("Initializing database with SQLAlchemy seed...")
            import seed_db
            seed_db.seed_database()

        # Unlike the block above, this always runs: it only inserts the
        # CyberLab challenge rows that are missing, so it's safe on every
        # startup (fresh DB or an existing one, e.g. database/hacktheai.db).
        import seed_cyberlab_challenges
        seed_cyberlab_challenges.seed_cyberlab_challenges()

        # Seed PRO Lab 01: The Ghost in the Ledger
        import seed_ghost_ledger
        seed_ghost_ledger.seed_ghost_ledger()

        # Seed PRO Lab 02: The Vanishing Consensus
        import seed_vanishing_consensus
        seed_vanishing_consensus.seed_vanishing_consensus()


    # Ensure upload directories exist
    upload_dir = app.config.get('LAB_UPLOAD_DIR', os.path.join(os.path.dirname(__file__), 'data', 'uploaded_labs'))
    os.makedirs(upload_dir, exist_ok=True)
    logger.info(f"Lab upload directory: {upload_dir}")


def _ensure_uploaded_labs_sort_order_column():
    """db.create_all() only creates missing tables, not new columns on
    tables that already exist. Deployments upgrading from before labs had
    a learning-path order need this column added and backfilled once."""
    from sqlalchemy import inspect as sa_inspect, text

    inspector = sa_inspect(db.engine)
    if 'uploaded_labs' not in inspector.get_table_names():
        return
    existing_columns = {c['name'] for c in inspector.get_columns('uploaded_labs')}
    if 'sort_order' in existing_columns:
        return

    logger.info("Adding sort_order column to uploaded_labs and backfilling by creation date...")
    with db.engine.begin() as conn:
        conn.execute(text('ALTER TABLE uploaded_labs ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0'))
        rows = conn.execute(text('SELECT id FROM uploaded_labs ORDER BY created_at ASC')).fetchall()
        for i, row in enumerate(rows, start=1):
            conn.execute(text('UPDATE uploaded_labs SET sort_order = :n WHERE id = :id'),
                         {'n': i, 'id': row[0]})

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint for load balancers."""
    try:
        # Check DB connection
        db.session.execute(db.text('SELECT 1'))
        db_status = "ok"
    except Exception as e:
        logger.error(f"Health check DB error: {e}")
        db_status = "error"
        
    return jsonify({
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status
    }), 200 if db_status == "ok" else 503

db_initialized = False

@app.before_request
def initialize_database():
    global db_initialized
    if not db_initialized:
        try:
            init_db()
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
        db_initialized = True

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=5000)
