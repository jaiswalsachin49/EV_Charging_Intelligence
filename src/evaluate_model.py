import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

# Load Data
df = pd.read_csv("data/processed/ev_charging_processed.csv")

# Define features (same as training)
target = 'utilization_rate'
numeric_features = [
    'traffic_congestion_index', 'gas_price_per_gallon', 'temperature_f', 
    'precipitation_mm', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_peak_hour'
]
categorical_features = [
    'weather_category', 'location_type', 'charger_type', 'city', 'local_event'
]

X = df[numeric_features + categorical_features]
y = df[target]

# Split Data (same random_state as training to ensure valid test set)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load Model
model = joblib.load("models/demand_predictor.pkl")

# Predict
y_pred = model.predict(X_test)

# Calculate Metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2: {r2:.4f}")
