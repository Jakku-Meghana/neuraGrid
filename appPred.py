import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from tensorflow.keras.models import load_model
from datetime import timedelta

np.random.seed(42)

# ============================================================
# CONFIG
# ============================================================
PAST_STEPS = 30
FORECAST_DAYS = 7

MODEL_PATH = "models/gru_daily_load.h5"
SCALER_PATH = "models/scaler.pkl"
DATA_PATH = "telangana_demand_weather_final.csv"

# ============================================================
# LOAD MODEL & SCALER
# ============================================================
gru = load_model(MODEL_PATH, compile=False)
scaler = joblib.load(SCALER_PATH)

feature_cols = [
    "demand",
    "temperature",
    "humidity",
    "rain",
    "cloud",
    "windspeed",
    "dayofweek",
    "is_weekend",
    "is_holiday"
]

load_idx = feature_cols.index("demand")

print("✅ GRU model & scaler loaded (CPU)")
print("Feature order:", feature_cols)

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv(DATA_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df.sort_values("timestamp", inplace=True)
df.reset_index(drop=True, inplace=True)

# ============================================================
# TIME FEATURES
# ============================================================
df["dayofweek"] = df["timestamp"].dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
df["is_holiday"] = 0

# ============================================================
# SCALE DATA
# ============================================================
scaled_df = pd.DataFrame(
    scaler.transform(df[feature_cols]),
    columns=feature_cols
)

last_sequence = scaled_df.values[-PAST_STEPS:].reshape(
    1, PAST_STEPS, len(feature_cols)
)

# ============================================================
# STATISTICAL ANCHORS
# ============================================================
BASELINE_LOAD = df["demand"].rolling(30).mean().iloc[-1]
HIST_MIN = df["demand"].quantile(0.05)
HIST_MAX = df["demand"].quantile(0.95)

# ============================================================
# 🔮 NEXT 1 DAY PREDICTION (NON-LINEAR)
# ============================================================
def predict_next_day():
    pred_scaled = gru.predict(last_sequence, verbose=0)[0, 0]

    helper = np.zeros((1, len(feature_cols)))
    helper[0, load_idx] = pred_scaled
    pred_load = scaler.inverse_transform(helper)[0, load_idx]

    # ---- Non-linearity ----
    pred_load = 0.7 * pred_load + 0.3 * BASELINE_LOAD
    pred_load *= 1 + np.random.normal(0, 0.015)
    pred_load = np.clip(pred_load, HIST_MIN, HIST_MAX)

    return pred_load

# ============================================================
# 🔁 NEXT 7 DAYS ROLLING FORECAST (FIXED)
# ============================================================
def predict_next_7_days():
    preds = []
    seq = last_sequence.copy()
    current_date = pd.Timestamp.today().normalize()

    last_real_load = df["demand"].iloc[-1]
    weather_cols = ["temperature", "humidity", "rain", "cloud", "windspeed"]
    base_weather = df.iloc[-1][weather_cols]

    for i in range(FORECAST_DAYS):

        # ----------------- GRU Prediction -----------------
        pred_scaled = gru.predict(seq, verbose=0)[0, 0]
        helper = np.zeros((1, len(feature_cols)))
        helper[0, load_idx] = pred_scaled
        pred_load = scaler.inverse_transform(helper)[0, load_idx]

        # ----------------- NON-LINEAR FIXES -----------------

        # 1️⃣ Momentum
        momentum = pred_load - last_real_load
        pred_load += 0.4 * momentum

        # 2️⃣ Weather evolution
        weather = base_weather.copy()
        weather["temperature"] += np.random.normal(0, 1.2)
        weather["humidity"] += np.random.normal(0, 3.5)

        temp_effect = 1 + 0.02 * (weather["temperature"] - 30)
        humidity_effect = 1 + 0.01 * (weather["humidity"] - 60)

        pred_load *= temp_effect * humidity_effect

        # 3️⃣ Mean reversion (adaptive)
        deviation = abs(pred_load - BASELINE_LOAD) / BASELINE_LOAD
        reversion = min(deviation, 0.3)
        pred_load = (1 - reversion) * pred_load + reversion * BASELINE_LOAD

        # 4️⃣ Weekly seasonality
        pred_load *= 1 + 0.04 * np.sin(2 * np.pi * i / 7)

        # 5️⃣ Noise
        pred_load += np.random.normal(0, 0.012 * pred_load)

        # 6️⃣ Safety bounds
        pred_load = np.clip(pred_load, HIST_MIN, HIST_MAX)

        preds.append(pred_load)
        last_real_load = pred_load

        # ----------------- UPDATE INPUT SEQUENCE -----------------
        next_row = seq[0, -1].copy()

        helper[0, load_idx] = pred_load
        next_row[load_idx] = scaler.transform(helper)[0, load_idx]

        for col in weather_cols:
            idx = feature_cols.index(col)
            helper = np.zeros((1, len(feature_cols)))
            helper[0, idx] = weather[col]
            next_row[idx] = scaler.transform(helper)[0, idx]

        dow = current_date.dayofweek
        next_row[feature_cols.index("dayofweek")] = dow
        next_row[feature_cols.index("is_weekend")] = int(dow >= 5)
        next_row[feature_cols.index("is_holiday")] = 0

        seq = np.concatenate(
            [seq[:, 1:, :], next_row.reshape(1, 1, -1)],
            axis=1
        )

        current_date += timedelta(days=1)

    return np.array(preds)