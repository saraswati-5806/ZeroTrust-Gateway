import os
from flask import Flask, request, jsonify, g
from auth import generate_token, revoke_token
from middleware import zero_trust_interceptor

app = Flask(__name__)

# Register global Zero-Trust middleware
app.before_request(zero_trust_interceptor)

# Mock user database for demonstration
MOCK_USERS = {
    "admin": {"password": "adminpassword123", "role": "admin"},
    "operator": {"password": "operatorpassword123", "role": "operator"}
}

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "Zero-Trust Gateway"}), 200

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    user = MOCK_USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Unauthorized", "message": "Invalid credentials."}), 401

    token = generate_token(user_id=username, role=user["role"])
    return jsonify({
        "message": "Authentication successful.",
        "access_token": token,
        "token_type": "Bearer"
    }), 200

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    token = getattr(g, "token", None)
    if token and revoke_token(token):
        return jsonify({"message": "Successfully logged out and token invalidated."}), 200
    return jsonify({"error": "Bad Request", "message": "Failed to revoke token."}), 400

@app.route("/api/protected/dashboard", methods=["GET"])
def protected_dashboard():
    return jsonify({
        "message": "Access granted to Zero-Trust protected resource.",
        "user": g.user_id,
        "role": g.user_role
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)