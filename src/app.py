import streamlit as st
import pandas as pd
import joblib
import os

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="EV Charging Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS — Premium Dark Theme
# ==========================================
st.markdown("""
<style>
    /* ===== Google Font ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== Root Variables ===== */
    :root {
        --bg-primary: #0a0e1a;
        --bg-card: rgba(17, 24, 45, 0.85);
        --bg-card-hover: rgba(25, 35, 60, 0.95);
        --accent-green: #00e676;
        --accent-blue: #448aff;
        --accent-purple: #7c4dff;
        --accent-orange: #ff9100;
        --accent-red: #ff5252;
        --accent-cyan: #18ffff;
        --text-primary: #e8eaf6;
        --text-secondary: #9fa8da;
        --border-subtle: rgba(255,255,255,0.06);
        --glow-green: 0 0 25px rgba(0,230,118,0.25);
        --glow-blue: 0 0 25px rgba(68,138,255,0.25);
    }

    /* ===== Global ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        max-width: 1200px;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1327 0%, #111b38 100%) !important;
        border-right: 1px solid var(--border-subtle);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
    }

    /* ===== Hero Banner ===== */
    .hero-banner {
        background: linear-gradient(135deg, #0d1b3e 0%, #1a1040 40%, #0d2818 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(0,230,118,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-banner h1 {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero-banner p {
        color: var(--text-secondary);
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
    }

    /* ===== Metric Cards ===== */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.5rem 1.5rem 1.2rem;
        text-align: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        backdrop-filter: blur(10px);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--glow-blue);
    }
    .metric-card .label {
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-card .sub {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
    }

    /* Card color accents */
    .card-green { border-left: 3px solid var(--accent-green); }
    .card-green .value { color: var(--accent-green); }
    .card-blue { border-left: 3px solid var(--accent-blue); }
    .card-blue .value { color: var(--accent-blue); }
    .card-orange { border-left: 3px solid var(--accent-orange); }
    .card-orange .value { color: var(--accent-orange); }
    .card-purple { border-left: 3px solid var(--accent-purple); }
    .card-purple .value { color: var(--accent-purple); }
    .card-red { border-left: 3px solid var(--accent-red); }
    .card-red .value { color: var(--accent-red); }
    .card-cyan { border-left: 3px solid var(--accent-cyan); }
    .card-cyan .value { color: var(--accent-cyan); }

    /* ===== Demand Gauge ===== */
    .gauge-container {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 2rem 2rem 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .gauge-bar-bg {
        width: 100%;
        height: 14px;
        background: rgba(255,255,255,0.06);
        border-radius: 7px;
        overflow: hidden;
        margin: 1rem 0 0.6rem;
    }
    .gauge-bar-fill {
        height: 100%;
        border-radius: 7px;
        transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
    }
    .gauge-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===== Insight Cards ===== */
    .insight-box {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin: 1.5rem 0;
    }
    .insight-box h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.8rem;
    }
    .insight-item {
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--border-subtle);
    }
    .insight-item:last-child {
        border-bottom: none;
    }
    .insight-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-top: 6px;
        flex-shrink: 0;
    }
    .insight-text {
        font-size: 0.92rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ===== Model Badge ===== */
    .model-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0,230,118,0.08);
        border: 1px solid rgba(0,230,118,0.2);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.82rem;
        color: var(--accent-green);
        margin-bottom: 1rem;
    }

    /* ===== Input Summary ===== */
    .input-summary {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin: 0.5rem 0;
    }
    .input-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 0.8rem;
    }
    .input-chip {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.8rem;
    }
    .input-chip .chip-label {
        color: var(--text-secondary);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .input-chip .chip-value {
        color: #ffffff;
        font-weight: 500;
        margin-top: 2px;
    }

    /* ===== Section Divider ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
        margin: 1.5rem 0;
    }

    /* ===== Hide default Streamlit elements ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Style the button */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(68,138,255,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(68,138,255,0.5) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# PATHS & LOADING
# ==========================================
MODEL_PATH = "models/demand_predictor.pkl"
DATA_PATH = "data/processed/ev_charging_final.csv"

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None

model = load_model()
df = load_data()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## ⚡ Controls")
    st.caption("Tune conditions to simulate demand.")
    st.markdown("---")

    # Temporal
    st.markdown("#### 🕒 Time & Date")
    hour = st.slider("Hour of Day", 0, 23, 17)
    day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    day_val = st.selectbox("Day of Week", list(day_map.keys()), format_func=lambda x: day_map[x], index=4)
    is_weekend = day_val >= 5
    is_peak = (7 <= hour <= 10) or (16 <= hour <= 19)
    if is_peak:
        st.success("⚡ Peak Hours Active")
    st.markdown("---")

    # Environment
    st.markdown("#### ⛅ Environment")
    temp_f = st.slider("Temperature (°F)", 0, 120, 85)
    precip = st.number_input("Precipitation (mm)", 0.0, 50.0, 0.0)
    weather_opts = sorted(df['weather_category'].unique().tolist()) if df is not None else ['Good', 'Bad', 'Neutral', 'Extreme']
    weather = st.selectbox("Weather", weather_opts)
    st.markdown("---")

    # Context
    st.markdown("#### 🚗 Traffic & Economics")
    traffic = st.select_slider("Traffic Congestion", options=[1, 2, 3], value=2, help="1: Low · 2: Medium · 3: High")
    gas_price = st.number_input("Gas Price ($/gal)", 2.0, 7.0, 4.50)
    event_opts = sorted(df['local_event'].unique().tolist()) if df is not None else ['none', 'concert', 'game']
    event = st.selectbox("Local Event", event_opts)
    st.markdown("---")

    # Station
    st.markdown("#### 📍 Station")
    city_opts = sorted(df['city'].unique().tolist()) if df is not None else ['San Francisco']
    city = st.selectbox("City", city_opts)
    loc_type_opts = sorted(df['location_type'].unique().tolist()) if df is not None else ['Urban Center']
    loc_type = st.selectbox("Location Type", loc_type_opts)
    charger_opts = sorted(df['charger_type'].unique().tolist()) if df is not None else ['DC Fast']
    charger = st.selectbox("Charger Type", charger_opts)


# ==========================================
# HERO BANNER
# ==========================================
st.markdown("""
<div class="hero-banner">
    <h1>⚡ EV Charging Intelligence</h1>
    <p>AI-Powered Demand Prediction & Infrastructure Planning</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# MODEL STATUS
# ==========================================
if model is None:
    st.markdown("""
    <div class="metric-card card-red" style="text-align:center; padding:2rem;">
        <div class="value" style="font-size:1.8rem;">❌ Model Not Found</div>
        <div class="sub">Run <code>python3 src/model_trainer.py</code> first to train the model.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Model badge
st.markdown("""
<div class="model-badge">
    <span>🟢</span>
    <span>Random Forest · R² 0.943 · 13 Features</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PREDICTION
# ==========================================
input_data = pd.DataFrame({
    'traffic_congestion_index': [traffic],
    'gas_price_per_gallon': [gas_price],
    'temperature_f': [temp_f],
    'precipitation_mm': [precip],
    'hour_of_day': [hour],
    'day_of_week': [day_val],
    'is_weekend': [is_weekend],
    'is_peak_hour': [is_peak],
    'weather_category': [weather],
    'location_type': [loc_type],
    'charger_type': [charger],
    'city': [city],
    'local_event': [event]
})

predict_btn = st.button("🚀  Predict Demand", type="primary", use_container_width=True)

if predict_btn:
    prediction = model.predict(input_data)[0]
    prediction = max(0.0, min(1.0, prediction))
    pct = prediction * 100

    # Determine demand level, color, label
    if prediction <= 0.3:
        level, color, bar_color, emoji = "Low", "var(--accent-green)", "linear-gradient(90deg, #00e676, #69f0ae)", "🟢"
    elif prediction <= 0.6:
        level, color, bar_color, emoji = "Moderate", "var(--accent-orange)", "linear-gradient(90deg, #ff9100, #ffc107)", "🟡"
    else:
        level, color, bar_color, emoji = "High", "var(--accent-red)", "linear-gradient(90deg, #ff5252, #ff1744)", "🔴"

    # ---------- METRIC CARDS ----------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card_class = "card-green" if prediction <= 0.3 else ("card-orange" if prediction <= 0.6 else "card-red")
        st.markdown(f"""
        <div class="metric-card {card_class}">
            <div class="label">Predicted Utilization</div>
            <div class="value">{pct:.1f}%</div>
            <div class="sub">Station capacity in use</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card card-blue">
            <div class="label">Demand Level</div>
            <div class="value">{emoji} {level}</div>
            <div class="sub">Based on all features</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        traffic_labels = {1: "Low", 2: "Medium", 3: "High"}
        traffic_colors = {1: "card-green", 2: "card-orange", 3: "card-red"}
        st.markdown(f"""
        <div class="metric-card {traffic_colors[traffic]}">
            <div class="label">Traffic Index</div>
            <div class="value">{traffic_labels[traffic]}</div>
            <div class="sub">Congestion level</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card card-cyan">
            <div class="label">Weather</div>
            <div class="value">{weather}</div>
            <div class="sub">{temp_f}°F · {precip}mm rain</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- DEMAND GAUGE ----------
    st.markdown(f"""
    <div class="gauge-container">
        <div style="font-size:0.85rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:1.5px; font-weight:500;">
            Demand Gauge
        </div>
        <div style="font-size:2.8rem; font-weight:800; color:{color}; margin:0.3rem 0;">{pct:.1f}%</div>
        <div class="gauge-bar-bg">
            <div class="gauge-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
        </div>
        <div class="gauge-labels">
            <span>0% — Idle</span>
            <span>50% — Balanced</span>
            <span>100% — Full</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- INSIGHTS ----------
    reasons = []
    if is_peak:
        reasons.append(("var(--accent-orange)", "⏰ <b>Peak Hours</b> — Demand typically surges between 7–10 AM and 4–7 PM."))
    if traffic == 3:
        reasons.append(("var(--accent-red)", "🚗 <b>High Traffic</b> — Congested routes increase nearby station usage."))
    if weather == 'Extreme':
        reasons.append(("var(--accent-red)", "🌡️ <b>Extreme Weather</b> — Temperature stress drives EV battery drain and charging need."))
    elif weather == 'Bad':
        reasons.append(("var(--accent-orange)", "🌧️ <b>Bad Weather</b> — Rain/snow may reduce foot-traffic but increase commuter charging."))
    if event != 'none':
        reasons.append(("var(--accent-purple)", f"🎪 <b>Local Event ({event.title()})</b> — Events attract vehicles, increasing demand."))
    if gas_price >= 5.5:
        reasons.append(("var(--accent-green)", "⛽ <b>High Gas Price</b> — Expensive fuel pushes more drivers toward EV charging."))
    if is_weekend:
        reasons.append(("var(--accent-blue)", "📅 <b>Weekend</b> — Different demand patterns compared to weekdays."))

    if reasons:
        items_html = ""
        for dot_color, text in reasons:
            items_html += '<div class="insight-item"><div class="insight-dot" style="background:' + dot_color + ';"></div><div class="insight-text">' + text + '</div></div>'
        full_html = '<div class="insight-box"><h3>💡 Key Demand Drivers</h3>' + items_html + '</div>'
        st.markdown(full_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-box"><h3>💡 Key Demand Drivers</h3><div class="insight-item"><div class="insight-dot" style="background:var(--accent-green);"></div><div class="insight-text">Conditions are <b>normal</b>. Demand follows standard daily patterns with no notable surges expected.</div></div></div>', unsafe_allow_html=True)

    # ---------- INPUT SUMMARY ----------
    with st.expander("🔍 View Simulation Parameters"):
        st.markdown(f"""
        <div class="input-summary">
            <div class="input-grid">
                <div class="input-chip"><div class="chip-label">City</div><div class="chip-value">{city}</div></div>
                <div class="input-chip"><div class="chip-label">Location</div><div class="chip-value">{loc_type}</div></div>
                <div class="input-chip"><div class="chip-label">Charger</div><div class="chip-value">{charger}</div></div>
                <div class="input-chip"><div class="chip-label">Hour</div><div class="chip-value">{hour}:00</div></div>
                <div class="input-chip"><div class="chip-label">Day</div><div class="chip-value">{day_map[day_val]}</div></div>
                <div class="input-chip"><div class="chip-label">Weekend</div><div class="chip-value">{'Yes' if is_weekend else 'No'}</div></div>
                <div class="input-chip"><div class="chip-label">Peak Hour</div><div class="chip-value">{'Yes' if is_peak else 'No'}</div></div>
                <div class="input-chip"><div class="chip-label">Temperature</div><div class="chip-value">{temp_f}°F</div></div>
                <div class="input-chip"><div class="chip-label">Precipitation</div><div class="chip-value">{precip} mm</div></div>
                <div class="input-chip"><div class="chip-label">Weather</div><div class="chip-value">{weather}</div></div>
                <div class="input-chip"><div class="chip-label">Traffic</div><div class="chip-value">Level {traffic}</div></div>
                <div class="input-chip"><div class="chip-label">Gas Price</div><div class="chip-value">${gas_price:.2f}</div></div>
                <div class="input-chip"><div class="chip-label">Event</div><div class="chip-value">{event.title()}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div class="gauge-container" style="padding:3rem 2rem;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">🔮</div>
        <div style="font-size:1.1rem; font-weight:500; color:var(--text-primary); margin-bottom:0.4rem;">
            Ready to Predict
        </div>
        <div style="font-size:0.88rem; color:var(--text-secondary);">
            Adjust the simulation controls in the sidebar, then hit <b>Predict Demand</b> to see the AI forecast.
        </div>
    </div>
    """, unsafe_allow_html=True)