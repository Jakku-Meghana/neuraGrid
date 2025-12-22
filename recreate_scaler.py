import joblib
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import os

# Load the data
df = pd.read_csv('telangana_demand_weather_final.csv')
df["timestamp"] = pd.to_datetime(df["timestamp"])
df.sort_values("timestamp", inplace=True)
df.reset_index(drop=True, inplace=True)

# Add features
df["dayofweek"] = df["timestamp"].dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
df["is_holiday"] = 0

feature_cols = ['demand', 'temperature', 'humidity', 'rain', 'cloud', 'windspeed', 'dayofweek', 'is_weekend', 'is_holiday']

# Fit the scaler
scaler = StandardScaler()
scaler.fit(df[feature_cols])

# Save to models folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)
scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
joblib.dump(scaler, scaler_path)

print(f"Scaler recreated successfully at {scaler_path}")
