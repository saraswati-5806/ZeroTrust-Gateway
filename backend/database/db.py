import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any
import jwt

# Attempt Redis connection for token revocation; fall back to in-memory set if unavailable
try:
    import redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    redis_client.ping()
    USE_REDIS = True
except Exception:
    redis_client = None
    USE_REDIS = False

# File Paths & Secrets Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MICRO_APPS_FILE = os.path.join(BASE_DIR, "micro_apps.json")
ACCESS_LOGS_FILE = os.path.join(BASE_DIR, "access_logs.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "zero-trust-gateway-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 2

# In-memory blocklist fallback
_IN_MEMORY_BLOCKLIST: set = set()


# ------------------------------------------------------------------
# 1. Base JSON I/O Helpers
# ------------------------------------------------------------------

def _read_json_file(file_path: str, default_content: Any = None) -> Any:
    """Reads and parses a target JSON file safely."""
    if not os.path.exists(file_path):
        return default_content if default_content is not None else []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default_content if default_content is not None else []


def _write_json_file(file_path: str, data: Any) -> None:
    """Writes formatted data to a target JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ------------------------------------------------------------------
# 2. Authentication & PyJWT Logic
# ------------------------------------------------------------------

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Validates credentials against backend/database/users.json."""
    users = _read_json_file(USERS_FILE, default_content=[])
    for user in users:
        if user.get("username") == username and user.get("password") == password:
            return {
                "username": user["username"],
                "role": user.get("role", "user"),
                "device_id": user.get("device_id", "unknown")
            }
    return None


def generate_token(username: str, role: str) -> str:
    """Generates a signed JWT with a unique JTI claim for revocation."""
    now = datetime.now(timezone.utc)
    payload = {
        "jti": str(uuid.uuid4()),
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_and_validate_token(token: str) -> Dict[str, Any]:
    """Decodes JWT and checks against the Redis/in-memory blocklist."""
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    jti = payload.get("jti")

    if jti:
        if USE_REDIS and redis_client:
            if redis_client.get(f"blocklist:{jti}"):
                raise jwt.InvalidTokenError("Token has been revoked.")
        elif jti in _IN_MEMORY_BLOCKLIST:
            raise jwt.InvalidTokenError("Token has been revoked.")

    return payload


def revoke_token(token: str) -> bool:
    """Revokes a JWT by adding its JTI to the blocklist."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
        jti = payload.get("jti")
        exp = payload.get("exp")

        if jti:
            if USE_REDIS and redis_client and exp:
                now = datetime.now(timezone.utc).timestamp()
                remaining_ttl = int(exp - now)
                if remaining_ttl > 0:
                    redis_client.setex(f"blocklist:{jti}", remaining_ttl, "revoked")
            else:
                _IN_MEMORY_BLOCKLIST.add(jti)
            return True
    except jwt.PyJWTError:
        pass
    return False


# ------------------------------------------------------------------
# 3. Micro-Apps Registry Handlers
# ------------------------------------------------------------------

def get_micro_apps() -> List[Dict[str, Any]]:
    """Reads protected micro-apps from backend/database/micro_apps.json."""
    return _read_json_file(MICRO_APPS_FILE, default_content=[])


def get_micro_app_by_id(app_id: str) -> Optional[Dict[str, Any]]:
    """Fetches a specific micro-app definition by ID."""
    apps = get_micro_apps()
    for app in apps:
        if app.get("id") == app_id:
            return app
    return None


# ------------------------------------------------------------------
# 4. Access Logging Handlers
# ------------------------------------------------------------------

def log_access_event(username: str, action: str, resource: str, status: str, risk_score: float = 0.0) -> Dict[str, Any]:
    """Appends new access records to backend/database/access_logs.json."""
    logs = _read_json_file(ACCESS_LOGS_FILE, default_content=[])

    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "username": username,
        "action": action,
        "resource": resource,
        "status": status,
        "risk_score": risk_score
    }

    logs.append(log_entry)
    _write_json_file(ACCESS_LOGS_FILE, logs)
    return log_entry


def get_access_logs() -> List[Dict[str, Any]]:
    """Retrieves all logged events."""
    return _read_json_file(ACCESS_LOGS_FILE, default_content=[])