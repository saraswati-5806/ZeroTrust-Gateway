import os
import joblib
import numpy as np

class RiskModelService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), 'saved_model.pkl')
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.scaler = data['scaler']
        else:
            self.model = None
            self.scaler = None

    def predict_risk(self, features_dict):
        """
        Takes a dict of features and returns a risk score between 0 and 100.
        """
        if not self.model or not self.scaler:
            base_score = 20
            if features_dict.get('device_known', 1) == 0:
                base_score += 40
            if features_dict.get('failed_attempts', 0) > 3:
                base_score += 30
            return min(base_score, 100)

        feature_vector = np.array([[
            features_dict.get('login_hour', 10),
            features_dict.get('failed_attempts', 0),
            features_dict.get('geo_distance_km', 0.0),
            features_dict.get('device_known', 1),
            features_dict.get('role_mismatch', 0)
        ]])

        X_scaled = self.scaler.transform(feature_vector)
        raw_score = self.model.decision_function(X_scaled)[0]
        
        risk_score = int(max(0, min(100, (0.5 - raw_score) * 100)))
        return risk_score

risk_service = RiskModelService()