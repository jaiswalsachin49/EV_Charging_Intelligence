import os
import pandas as pd

INPUT_PATH = "data/processed/ev_charging_sampled.csv"
OUTPUT_PATH = "data/processed/ev_charging_processed.csv"

def load_and_clean_data():
    if not os.path.exists(INPUT_PATH):
        print("Error: Input file not found")
        return None
    df = pd.read_csv(INPUT_PATH)
    print(f"    Original shape: {df.shape}")

    #Keeping only Operational Station
    if 'station_status' in df.columns:
        df = df[df['station_status'] == 'operational'].copy()
        print(f"   Filtered to {len(df)} operational stations.")
    
    #Dropping Duplicates
    df.drop_duplicates(subset=['station_id', 'timestamp'], keep='first', inplace=True)
    print(f"   Shape after dropping duplicates: {df.shape}")
    
    #Date Time Conversion
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp')

    #Feature Engineering
    print("   Engineering Weather Features...")
    def simplify_weather(w):
        w = str(w).lower()
        if 'rain' in w or 'snow' in w or 'storm' in w or 'freezing' in w:
            return 'Bad'
        elif 'extreme_heat' in w:
            return 'Extreme' 
        elif 'cloud' in w or 'overcast' in w:
            return 'Neutral'
        else:
            return 'Good' 
            
    if 'weather_condition' in df.columns:
        df['weather_category'] = df['weather_condition'].apply(simplify_weather)
    else:
        df['weather_category'] = 'Unknown'


    # Keep only what is necessary for the Machine Learning Model.
    keep_columns = [
        'utilization_rate',         # TARGET VARIABLE
        'traffic_congestion_index', # Feature 1 (Context)
        'gas_price_per_gallon',     # Feature 2 (Economic)
        'temperature_f',            # Feature 3 (Environmental)
        'precipitation_mm',         # Feature 4 (Environmental)
        'hour_of_day',              # Feature 5 (Temporal)
        'day_of_week',              # Feature 6 (Temporal)
        'is_weekend',               # Feature 7 (Temporal)
        'is_peak_hour',             # Feature 8 (Temporal)
        'local_event',              # Feature 9 (Context)
        'weather_category',         # Feature 10 (Engineered)
        'location_type',            # Feature 11 (Categorical)
        'charger_type',             # Feature 12 (Categorical)
        'city',                     # For Location Context
        'latitude',
        'longitude'
    ]
    
    # Filter columns that actually exist in the dataframe
    existing_cols = [c for c in keep_columns if c in df.columns]
    df_final = df[existing_cols].copy()

    #Drop any remaining rows with missing values    
    df_final = df_final.dropna()

    # 6. SAVE TO DISK
    df_final.to_csv(OUTPUT_PATH, index=False)
    print(f"SUCCESS! Cleaned data saved to: {OUTPUT_PATH}")
    print(f"   Final Shape: {df_final.shape}")
    print("-" * 30)
    print("   Top 3 Rows:")
    print(df_final[['utilization_rate', 'traffic_congestion_index', 'weather_category', 'is_peak_hour']].head(3))
    print("-" * 30)

if __name__ == "__main__":
    load_and_clean_data()