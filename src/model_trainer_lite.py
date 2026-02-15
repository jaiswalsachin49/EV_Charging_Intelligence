import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Load Data
print("⏳ Loading data...")
DATA_PATH = "data/processed/ev_charging_processed.csv"
if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} not found.")
    exit(1)
    
df = pd.read_csv(DATA_PATH)

# Define Features
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

# Build Pipeline (matches app.py expectation)
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Lite Model Configuration
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(
        n_estimators=50,      # Reduced trees
        max_depth=10,         # Restricted depth
        n_jobs=-1,
        random_state=42
    ))
])

# Train
print("⚙️ Training LITE model with Pipeline...")
model_pipeline.fit(X, y)

# Save
print("💾 Saving model...")
# Compress=3 reduces size significantly
joblib.dump(model_pipeline, "models/demand_predictor.pkl", compress=3) 
print("✅ Done! New LITE Pipeline model saved to models/demand_predictor.pkl")