import os
from dotenv import load_dotenv
import secrets

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_or_create_persistent_secret_key():
    """Resolve SECRET_KEY, falling back to a value persisted on disk
    or a stable fallback instead of a fresh random one every request.

    A brand-new random key on every process start breaks every existing
    session and CSRF token on serverless platforms (like Vercel).
    """
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key

    # Vercel / Serverless environment check
    if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
        return os.environ.get('SECRET_KEY', 'hacktheai-vercel-prod-secret-9f82d1c4b7a3e6f50123456789abcdef')

    key_path = os.path.join(BASE_DIR, 'database', '.secret_key')
    try:
        if os.path.exists(key_path):
            with open(key_path, 'r') as f:
                existing = f.read().strip()
            if existing:
                return existing
    except OSError:
        pass

    fallback_static_key = 'hacktheai-persistent-secret-key-v1-prod-2026-auth'
    new_key = secrets.token_hex(32)
    try:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        # Exclusive create so a race between multiple workers starting at
        # once can't have one worker overwrite another's freshly-written key.
        fd = os.open(key_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'w') as f:
            f.write(new_key)
        return new_key
    except FileExistsError:
        # Another worker won the race and wrote it first - read what it wrote.
        with open(key_path, 'r') as f:
            return f.read().strip()
    except OSError:
        # On read-only filesystem (e.g. serverless containers), return static fallback
        return fallback_static_key


class Config:
    """Base configuration."""
    SECRET_KEY = _get_or_create_persistent_secret_key()

    # Database
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'hacktheai.db')
    # Database setup: use /tmp on Vercel since it's the only writable directory
    if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
        DATABASE_PATH = '/tmp/hacktheai.db'
    else:
        DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'hacktheai.db')
        
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Tuning for connection pooling under load
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
    }
    if not SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        SQLALCHEMY_ENGINE_OPTIONS["pool_size"] = 20
        SQLALCHEMY_ENGINE_OPTIONS["max_overflow"] = 10
    
    # Rate Limiting
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "200 per day, 50 per hour")
    RATELIMIT_STORAGE_URI = "memory://" # Forced memory:// to prevent Redis connection timeouts on Vercel

    # CSRF tokens default to expiring after 1 hour (Flask-WTF's WTF_CSRF_TIME_LIMIT),
    # which is the same length as a lab session. A learner who spends a while
    # working through a multi-step lab before submitting their flag would get a
    # silently-expired token: the request fails with a generic-looking error that
    # has nothing to do with the flag itself. Tying token validity to the login
    # session instead (no fixed time limit) avoids that entirely.
    WTF_CSRF_TIME_LIMIT = None

    # Secure Cookie settings. Forcing `Secure` on the session cookie when the
    # app isn't actually served over HTTPS makes browsers silently refuse to
    # store it at all - every request then looks like a brand new, logged-out
    # session. This must only turn on when the deployment genuinely terminates
    # TLS somewhere in front of it (set FORCE_HTTPS=true once that's true).
    FORCE_HTTPS = os.environ.get('FORCE_HTTPS', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = FORCE_HTTPS

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # In dev, we might not have HTTPS
    SESSION_COOKIE_SECURE = False

    # Lab Engine Config
    LAB_UPLOAD_MAX_SIZE = 100 * 1024 * 1024  # 100MB
    LAB_UPLOAD_DIR = os.path.join(BASE_DIR, 'data', 'uploaded_labs')
    LAB_CONTAINER_PORT_MIN = 10000
    LAB_CONTAINER_PORT_MAX = 20000
    LAB_SESSION_TIMEOUT = 3600  # 1 hour in seconds
    LAB_MAX_CONCURRENT_SESSIONS = 50
    LAB_MAX_ZIP_DECOMPRESSED_SIZE = 500 * 1024 * 1024  # 500MB
    LAB_MAX_ZIP_FILE_COUNT = 10000

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Only actually forces Secure cookies / HTTPS redirects when the
    # deployment has set FORCE_HTTPS=true (see Config.FORCE_HTTPS above).
    # Defaulting this to True unconditionally breaks any production
    # deployment that doesn't yet have TLS terminated in front of it
    # (e.g. the bundled nginx config, which ships with its HTTPS server
    # block commented out until certs are mounted).
    SESSION_COOKIE_SECURE = Config.FORCE_HTTPS
    # Ensure SECRET_KEY is strictly enforced in production in the future.

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    default=ProductionConfig
)

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])
