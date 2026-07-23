import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

def train_isolation_forest():
    csv_path = os.path.join(os.path.dirname(__file__), '../backend/data/access_logs.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Training data not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    # Select features matching the access log dataset structure
    features = ['login_hour', 'failed_attempts', 'geo_distance_km', 'device_known', 'role_mismatch']
    X = df[features].fillna(0)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest model for anomaly detection
    clf = IsolationForest(contamination=0.2, random_state=42)
    clf.fit(X_scaled)
    
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, 'saved_model.pkl')
    
    joblib.dump({'model': clf, 'scaler': scaler}, model_path)
    print(f"Model successfully trained and saved to {model_path}")

if __name__ == '__main__':
    train_isolation_forest()