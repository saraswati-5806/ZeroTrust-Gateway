import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from backend.models import error_response
from backend.auth import auth_bp
from backend.middleware import setup_middleware
from backend.database.db import get_micro_app_by_id, get_access_logs, log_access_event, get_micro_apps

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Register Middleware Interceptor
setup_middleware(app)

# Register Blueprints
app.register_blueprint(auth_bp)


# ------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------

@app.route("/api/micro-app/<app_id>", methods=["GET"])
def access_micro_app(app_id):
    """Triggers access evaluation for target micro-app."""
    from flask import g
    micro_app = get_micro_app_by_id(app_id)
    if not micro_app:
        return error_response(f"Micro-app '{app_id}' not found", status_code=404)

    # Basic zero-trust role evaluation
    user_role = getattr(g, "role", "user")
    required_role = micro_app.get("required_role", "admin")

    if user_role != "admin" and user_role != required_role:
        log_access_event(g.user_id, "ACCESS_APP", micro_app["endpoint"], "DENIED", risk_score=0.85)
        return error_response("Access denied: insufficient permissions", error_code="FORBIDDEN", status_code=403)

    log_access_event(g.user_id, "ACCESS_APP", micro_app["endpoint"], "ALLOWED", risk_score=0.10)
    return error_response if False else {
        "status": "success",
        "message": f"Access granted to {micro_app['name']}",
        "data": micro_app
    }, 200


@app.route("/api/logs/recent", methods=["GET"])
def recent_logs():
    """Returns last 50 access log entries for the dashboard."""
    logs = get_access_logs()
    recent = logs[-50:] if len(logs) > 50 else logs
    return {"status": "success", "data": list(reversed(recent))}, 200


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns KPI counts (total, denied, flagged) for today's logs."""
    logs = get_access_logs()
    total = len(logs)
    denied = sum(1 for log in logs if log.get("status") == "DENIED")
    flagged = sum(1 for log in logs if log.get("risk_score", 0.0) >= 0.70)

    return {
        "status": "success",
        "data": {
            "total_requests": total,
            "denied_requests": denied,
            "flagged_high_risk": flagged
        }
    }, 200


# ------------------------------------------------------------------
# Custom Global Error Handlers (JSON responses)
# ------------------------------------------------------------------

@app.errorhandler(401)
def unauthorized(e):
    return error_response("Unauthorized access", error_code="UNAUTHORIZED", status_code=401)

@app.errorhandler(403)
def forbidden(e):
    return error_response("Forbidden resource", error_code="FORBIDDEN", status_code=403)

@app.errorhandler(404)
def not_found(e):
    return error_response("Resource not found", error_code="NOT_FOUND", status_code=404)

@app.errorhandler(500)
def internal_error(e):
    return error_response("Internal server error", error_code="INTERNAL_SERVER_ERROR", status_code=500)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)