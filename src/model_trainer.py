import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATA_PATH = "data/processed/ev_charging_processed.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "demand_predictor.pkl")

def train_model():
    if not os.path.exists(DATA_PATH):
        print("Error: Data file not found. Run data_preprocessing.py first.")
        return
    
    print("Loading Cleaned Data...")
    df = pd.read_csv(DATA_PATH)

    target = 'utilization_rate'
    numeric_features = [
        'traffic_congestion_index', 
        'gas_price_per_gallon',     
        'temperature_f',            
        'precipitation_mm',         
        'hour_of_day',              
        'day_of_week',              
        'is_weekend',               
        'is_peak_hour'
    ]
    categorical_features = [
        'weather_category',         
        'location_type',            
        'charger_type',             
        'city',                     
        'local_event'               
    ]

    print(f"   Training with {len(numeric_features + categorical_features)} features...")

    X = df[numeric_features + categorical_features]
    y = df[target]
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])

    print("✂️  Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🧠 Training Random Forest Model (Agents working)...")
    model_pipeline.fit(X_train, y_train)

    print("📊 Evaluating...")
    y_pred = model_pipeline.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("-" * 40)
    print(f"   ✅ Model Trained Successfully!")
    print(f"   📉 RMSE: {rmse:.4f} (Error Margin)")
    print(f"   🎯 R² Score: {r2:.4f} (Target: > 0.80)")
    print("-" * 40)

    # 7. Save
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model_pipeline, MODEL_PATH)
    print(f"💾 Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()