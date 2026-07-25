from flask import Blueprint, request, make_response, g
from backend.models import success_response, error_response
from backend.database.db import authenticate_user, generate_token, revoke_token, decode_and_validate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Validates credentials, generates JWT, and sets an httpOnly cookie."""
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response("Username and password are required", status_code=400)

    user = authenticate_user(username, password)
    if not user:
        return error_response("Invalid credentials", error_code="UNAUTHORIZED", status_code=401)

    token = generate_token(user["username"], user["role"])

    resp, status_code = success_response(
        data={
            "token": token,
            "user": {
                "username": user["username"],
                "role": user["role"],
                "device_id": user["device_id"]
            }
        },
        message="Login successful"
    )
    
    response = make_response(resp, status_code)
    response.set_cookie("access_token", token, httponly=True, samesite="Lax")
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Revokes active token by adding its JTI to Redis blocklist."""
    token = getattr(g, "token", None) or request.cookies.get("access_token")
    if token:
        revoke_token(token)

    response, status_code = success_response(message="Logged out successfully")
    res = make_response(response, status_code)
    res.delete_cookie("access_token")
    return res


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """Issues new token if current token is valid."""
    token = getattr(g, "token", None) or request.cookies.get("access_token")
    if not token:
        return error_response("Token required for refresh", status_code=401)

    try:
        payload = decode_and_validate_token(token)
        new_token = generate_token(payload["sub"], payload["role"])
        return success_response(data={"token": new_token}, message="Token refreshed")
    except Exception as e:
        return error_response(f"Cannot refresh token: {str(e)}", status_code=401)


@auth_bp.route("/me", methods=["GET"])
def get_me():
    """Returns current user context from JWT claims."""
    return success_response(data={
        "username": getattr(g, "user_id", None),
        "role": getattr(g, "role", None),
        "device_id": getattr(g, "device_id", None),
        "login_hour": getattr(g, "login_hour", None),
        "geo_country": getattr(g, "geo_country", None)
    })