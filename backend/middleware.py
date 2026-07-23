import requests
from datetime import datetime, timezone
from flask import request, g, current_app
from backend.models import error_response
from backend.database.db import decode_and_validate_token, get_micro_app_by_id, log_access_event

PUBLIC_ENDPOINTS = ["/auth/login", "/auth/refresh", "/health"]


def fetch_geo_country(ip_address: str) -> str:
    """Queries ip-api.com to resolve geo country from IP address."""
    if ip_address in ["127.0.0.1", "localhost", "::1"] or ip_address.startswith("192.168."):
        return "LOCAL"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=countryCode", timeout=2.0)
        if response.status_code == 200:
            return response.json().get("countryCode", "UNKNOWN")
    except Exception:
        pass
    return "UNKNOWN"


def setup_middleware(app):
    """Registers the before_request interceptor with the Flask application."""
    
    @app.before_request
    def interceptor():
        # Skip authentication for public endpoints
        if request.path in PUBLIC_ENDPOINTS or request.method == "OPTIONS":
            return None

        # 1. Extract Token from Authorization header or httpOnly cookie
        auth_header = request.headers.get("Authorization")
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        elif request.cookies.get("access_token"):
            token = request.cookies.get("access_token")

        if not token:
            return error_response("Missing authentication token", error_code="UNAUTHORIZED", status_code=401)

        # 2. Decode and Validate JWT Claims & Blocklist
        try:
            payload = decode_and_validate_token(token)
        except Exception as e:
            return error_response(f"Invalid or expired token: {str(e)}", error_code="UNAUTHORIZED", status_code=401)

        # 3. Extract Request Context & Perform Geo Lookup
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        geo_country = fetch_geo_country(client_ip)
        current_hour = datetime.now(timezone.utc).hour

        # 4. Attach Context to Flask 'g' Object
        g.user_id = payload.get("sub")
        g.role = payload.get("role")
        g.device_id = request.headers.get("X-Device-ID", "unknown-device")
        g.login_hour = current_hour
        g.geo_country = geo_country
        g.token = token

        return None