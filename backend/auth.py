import os
import uuid
from datetime import datetime, timedelta, timezone
import jwt
import redis

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "zero-trust-gateway-super-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 2

# Redis connection for token blocklist
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

def generate_token(user_id: str, role: str) -> str:
    """Generate a signed JWT with unique JTI claim for blocklisting."""
    now = datetime.now(timezone.utc)
    payload = {
        "jti": str(uuid.uuid4()),
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_and_validate_token(token: str) -> dict:
    """Validate JWT signature, expiration, and check Redis blocklist."""
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    
    jti = payload.get("jti")
    if jti and redis_client.get(f"blocklist:{jti}"):
        raise jwt.InvalidTokenError("Token has been revoked.")
        
    return payload

def revoke_token(token: str) -> bool:
    """Revoke a token by adding its JTI to the Redis blocklist with TTL."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
        jti = payload.get("jti")
        exp = payload.get("exp")
        
        if jti and exp:
            now = datetime.now(timezone.utc).timestamp()
            remaining_ttl = int(exp - now)
            
            if remaining_ttl > 0:
                redis_client.setex(f"blocklist:{jti}", remaining_ttl, "revoked")
            return True
    except jwt.PyJWTError:
        pass
    return False