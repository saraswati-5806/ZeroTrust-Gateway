import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

class AnomalyModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = None

    def train_and_save(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'access_logs.csv')
        df = pd.read_csv(csv_path)
        
        features = ['login_hour', 'failed_attempts', 'geo_distance_km', 'device_known', 'role_mismatch']
        X = df[features].fillna(0)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = IsolationForest(contamination=0.2, random_state=42)
        self.model.fit(X_scaled)
        
        # Ensure output directory exists
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ai'))
        os.makedirs(output_dir, exist_ok=True)
        
        model_path = os.path.join(output_dir, 'saved_model.pkl')
        joblib.dump({'model': self.model, 'scaler': self.scaler}, model_path)
        print(f"Anomaly model trained and saved successfully at {model_path}.")

if __name__ == '__main__':
    trainer = AnomalyModelTrainer()
    trainer.train_and_save()