import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.risk_model import risk_service
from ai.watsonx_client import watson_client

def evaluate_risk(context):
    """
    Evaluates incoming request context through the Isolation Forest model 
    and generates a human-readable threat explanation via watsonx.ai.
    """
    feature_payload = {
        "login_hour": context.get("login_hour", 10),
        "failed_attempts": context.get("failed_attempts", 0),
        "geo_distance_km": context.get("geo_distance_km", 0.0),
        "device_known": 1 if context.get("device_known", True) else 0,
        "role_mismatch": 1 if context.get("role_mismatch", False) else 0
    }
    
    risk_score = risk_service.predict_risk(feature_payload)
    
    if risk_score > 70:
        threat_label = "HIGH"
        decision = "DENY"
    elif risk_score >= 40:
        threat_label = "MEDIUM"
        decision = "FLAG"
    else:
        threat_label = "LOW"
        decision = "ALLOW"
        
    triggered_signals = []
    if feature_payload["device_known"] == 0:
        triggered_signals.append("UNKNOWN_DEVICE")
    if feature_payload["geo_distance_km"] > 1000:
        triggered_signals.append("GEO_ANOMALY")
    if feature_payload["login_hour"] < 6 or feature_payload["login_hour"] > 21:
        triggered_signals.append("TIME_VIOLATION")
    if feature_payload["role_mismatch"] == 1:
        triggered_signals.append("ROLE_MISMATCH")
        
    if not triggered_signals and risk_score < 40:
        triggered_signals.append("NORMAL_ACTIVITY")

    explanation_context = {
        "role": context.get("role", "user"),
        "app_name": context.get("app_name", "secure-portal"),
        "login_hour": feature_payload["login_hour"],
        "allowed_hours": "09:00 - 21:00",
        "geo_country": context.get("geo_country", "India"),
        "home_country": "India",
        "geo_distance_km": feature_payload["geo_distance_km"],
        "device_known": "Yes" if feature_payload["device_known"] == 1 else "No",
        "failed_attempts": feature_payload["failed_attempts"],
        "risk_score": risk_score,
        "decision": decision,
        "signals": triggered_signals
    }

    ai_explanation = watson_client.generate_explanation(explanation_context)

    return {
        "risk_score": risk_score,
        "threat_label": threat_label,
        "decision": decision,
        "reason": triggered_signals,
        "ai_explanation": ai_explanation
    }