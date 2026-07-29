import os
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai  # <--- Updated modern SDK import

from backend.models import error_response
from backend.auth import auth_bp
from backend.middleware import setup_middleware
from backend.database.db import get_micro_app_by_id, get_access_logs, log_access_event, get_micro_apps

load_dotenv()

# Initialize the official Gemini client (picks up GEMINI_API_KEY from environment automatically)
client = genai.Client()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Register Middleware Interceptor
setup_middleware(app)

# Register Blueprints
app.register_blueprint(auth_bp)


# ------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------

@app.route("/api/ai/analyze", methods=["POST"])
def analyze_threat():
    """Live AI threat analysis endpoint powered by Google Gemini."""
    try:
        data = request.get_json() or {}
        context = data.get("context", "Analyze current zero trust security posture and threat logs.")
        
        prompt = f"""
        You are an AI Security Operations Assistant inside an IBM Zero Trust Gateway.
        Analyze the following security context and provide a concise, actionable risk assessment:
        Context: {context}
        """
        
        # Use gemini-2.5-flash for fast, modern real-time analysis
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return {
            "status": "success",
            "analysis": response.text
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


@app.route("/api/micro-app/<app_id>", methods=["GET"])
def access_micro_app(app_id):
    """Triggers access evaluation for target micro-app."""
    micro_app = get_micro_app_by_id(app_id)
    if not micro_app:
        return error_response(f"Micro-app '{app_id}' not found", status_code=404)

    # Basic zero-trust role evaluation
    user_role = getattr(g, "role", "user")
    required_role = micro_app.get("required_role", "admin")

    if user_role != "admin" and user_role != required_role:
        log_access_event(getattr(g, "user_id", "anonymous"), "ACCESS_APP", micro_app.get("endpoint", app_id), "DENIED", risk_score=0.85)
        return error_response("Access denied: insufficient permissions", error_code="FORBIDDEN", status_code=403)

    log_access_event(getattr(g, "user_id", "anonymous"), "ACCESS_APP", micro_app.get("endpoint", app_id), "ALLOWED", risk_score=0.10)
    return {
        "status": "success",
        "message": f"Access granted to {micro_app.get('name', app_id)}",
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

@app.route("/", methods=["GET"])
def home():
    return {
        "status": "success",
        "message": "IBM Zero Trust Gateway API Running"
    }, 200

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "success",
        "message": "Zero Trust Gateway is running"
    }, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)