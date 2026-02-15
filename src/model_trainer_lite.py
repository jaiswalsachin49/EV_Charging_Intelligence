import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load Data
print("⏳ Loading data...")
df = pd.read_csv("data/processed/ev_charging_processed.csv")

# 1. Handle Categorical Columns (One-Hot Encoding)
# We need to convert text columns like 'weather_category', 'location_type' into numbers
categorical_cols = ['weather_category', 'location_type', 'charger_type', 'city', 'local_event']
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 2. Define Features (X) and Target (y)
# We drop the target ('utilization_rate') and any non-predictive columns (lat/long are usually not needed if we have city/location_type)
X = df.drop(['utilization_rate', 'latitude', 'longitude'], axis=1)
y = df['utilization_rate']

# 3. Train "Lite" Model
print("⚙️ Training LITE model...")
model = RandomForestRegressor(
    n_estimators=50,      # Small number of trees to keep file size low
    max_depth=10,         # Limit depth to prevent overfitting and reduce size
    n_jobs=-1,
    random_state=42
)
model.fit(X, y)

# 4. Save with Compression
print("💾 Saving model...")
joblib.dump(model, "models/demand_predictor.pkl", compress=3) 
print("✅ Done! New LITE model saved to models/demand_predictor.pkl")