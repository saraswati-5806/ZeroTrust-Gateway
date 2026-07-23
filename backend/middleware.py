from functools import wraps
from flask import request, jsonify, g
import jwt
from auth import decode_and_validate_token

EXEMPT_ROUTES = {"/api/auth/login", "/health"}

def zero_trust_interceptor():
    """Global before_request handler enforcing token authentication on non-exempt routes."""
    if request.path in EXEMPT_ROUTES or request.method == "OPTIONS":
        return None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized", "message": "Missing or malformed Authorization header."}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = decode_and_validate_token(token)
        # Store context in Flask's global state object for route handlers
        g.user_id = payload.get("sub")
        g.user_role = payload.get("role")
        g.token = token
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Unauthorized", "message": "Token has expired."}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": "Unauthorized", "message": str(e)}), 401
    except Exception:
        return jsonify({"error": "Internal Server Error", "message": "Authentication check failed."}), 500