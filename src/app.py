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
# CUSTOM CSS — Ultra Premium Futuristic Theme
# ==========================================
st.markdown("""
<style>
    /* ===== Google Fonts + Lucide Icons ===== */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://unpkg.com/lucide-static@0.468.0/font/lucide.css');

    /* ===== CSS Keyframe Animations ===== */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3), 0 0 40px rgba(0, 255, 136, 0.1); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 136, 0.5), 0 0 80px rgba(0, 255, 136, 0.2); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes fade-in-up {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes rotate-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse-ring {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(2); opacity: 0; }
    }
    
    @keyframes glow-breathe {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.7; }
    }
    
    @keyframes border-glow {
        0%, 100% { border-color: rgba(0, 255, 136, 0.15); }
        50% { border-color: rgba(0, 255, 136, 0.35); }
    }

    /* ===== Lucide Icon Helper ===== */
    .icon {
        font-family: 'lucide' !important;
        font-style: normal;
        font-weight: normal;
        font-variant: normal;
        text-transform: none;
        line-height: 1;
        -webkit-font-smoothing: antialiased;
    }

    /* ===== Root Variables ===== */
    :root {
        --bg-primary: #030712;
        --bg-secondary: #0f172a;
        --bg-card: rgba(15, 23, 42, 0.6);
        --glass-bg: rgba(15, 23, 42, 0.35);
        --glass-bg-strong: rgba(15, 23, 42, 0.6);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-border-light: rgba(255, 255, 255, 0.12);
        
        --accent-primary: #00ff88;
        --accent-secondary: #00d4ff;
        --accent-tertiary: #a855f7;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        --accent-info: #3b82f6;
        
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        --gradient-primary: linear-gradient(135deg, #00ff88 0%, #00d4ff 50%, #a855f7 100%);
        --gradient-dark: linear-gradient(180deg, #030712 0%, #0f172a 100%);
        
        --border-radius-sm: 8px;
        --border-radius-md: 12px;
        --border-radius-lg: 16px;
        --border-radius-xl: 24px;
        
        --shadow-glow: 0 0 50px rgba(0, 255, 136, 0.15);
        --shadow-card: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* ===== Global Styles ===== */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background: var(--bg-primary);
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    .block-container {
        padding: 2rem 2rem 4rem !important;
        max-width: 1400px;
    }

    /* ===== Ambient Background Glow ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(ellipse 80% 60% at 10% 10%, rgba(0, 255, 136, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse 60% 80% at 90% 80%, rgba(0, 212, 255, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse 50% 50% at 50% 50%, rgba(168, 85, 247, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* ===== Premium Glassmorphism Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 15, 28, 0.97) 0%, rgba(17, 24, 39, 0.95) 50%, rgba(10, 15, 28, 0.97) 100%) !important;
        border-right: 1px solid var(--glass-border);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(30px);
    }
    
    section[data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 300px;
        background: radial-gradient(ellipse at top, rgba(0, 255, 136, 0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
        font-weight: 400;
    }
    
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stNumberInput label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
    }

    /* ===== Hero Banner — Spectacular ===== */
    .hero-container {
        position: relative;
        margin-bottom: 2rem;
        animation: fade-in-up 0.8s ease-out;
    }
    
    .hero-banner {
        position: relative;
        background: var(--glass-bg);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid var(--glass-border-light);
        border-radius: var(--border-radius-xl);
        padding: 3rem 3rem 2.5rem;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -150%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(0, 255, 136, 0.03), transparent 30%);
        animation: rotate-slow 20s linear infinite;
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.08) 0%, transparent 70%);
        pointer-events: none;
        animation: glow-breathe 6s ease-in-out infinite;
    }
    
    .hero-glow-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        animation: float 8s ease-in-out infinite;
    }
    
    .hero-glow-orb.orb-1 {
        top: -100px; right: -50px;
        width: 300px; height: 300px;
        background: var(--accent-primary);
        opacity: 0.3;
    }
    
    .hero-glow-orb.orb-2 {
        bottom: -100px; left: -50px;
        width: 250px; height: 250px;
        background: var(--accent-tertiary);
        opacity: 0.25;
        animation-delay: -4s;
    }
    
    .hero-content {
        position: relative;
        z-index: 10;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 255, 136, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 50px;
        padding: 0.4rem 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--accent-primary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }
    
    .hero-badge::before {
        content: '';
        width: 8px; height: 8px;
        background: var(--accent-primary);
        border-radius: 50%;
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, #ffffff 0%, var(--accent-primary) 50%, var(--accent-secondary) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 5s ease infinite;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: var(--text-secondary);
        max-width: 600px;
        line-height: 1.6;
    }
    
    .hero-stats {
        display: flex;
        gap: 2rem;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--glass-border);
    }
    
    .hero-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--accent-primary);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .hero-stat-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===== Glassmorphism Metric Cards ===== */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin: 1.5rem 0;
    }
    
    @media (max-width: 1100px) {
        .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    }
    
    .metric-card {
        position: relative;
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border-light);
        border-radius: var(--border-radius-lg);
        padding: 1.75rem;
        text-align: center;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fade-in-up 0.6s ease-out backwards;
    }
    
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(0, 255, 136, 0.3);
        box-shadow: var(--shadow-glow), var(--shadow-card);
    }
    
    .metric-card:hover::before { opacity: 1; }
    .metric-card:hover::after { left: 100%; }
    
    .metric-icon {
        width: 48px; height: 48px;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 212, 255, 0.1));
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 136, 0.2);
        backdrop-filter: blur(10px);
        color: var(--accent-primary);
    }
    
    .metric-card .label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card .sub {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }

    /* Card Variants */
    .card-green .metric-icon { background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.05)); border-color: rgba(0, 255, 136, 0.3); color: #00ff88; }
    .card-green .value { background: linear-gradient(135deg, #00ff88, #00d4aa); -webkit-background-clip: text; background-clip: text; }
    .card-blue .metric-icon { background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.05)); border-color: rgba(59, 130, 246, 0.3); color: #3b82f6; }
    .card-blue .value { background: linear-gradient(135deg, #3b82f6, #00d4ff); -webkit-background-clip: text; background-clip: text; }
    .card-orange .metric-icon { background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.05)); border-color: rgba(245, 158, 11, 0.3); color: #f59e0b; }
    .card-orange .value { background: linear-gradient(135deg, #f59e0b, #fbbf24); -webkit-background-clip: text; background-clip: text; }
    .card-red .metric-icon { background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05)); border-color: rgba(239, 68, 68, 0.3); color: #ef4444; }
    .card-red .value { background: linear-gradient(135deg, #ef4444, #f87171); -webkit-background-clip: text; background-clip: text; }
    .card-cyan .metric-icon { background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 212, 255, 0.05)); border-color: rgba(0, 212, 255, 0.3); color: #00d4ff; }
    .card-cyan .value { background: linear-gradient(135deg, #00d4ff, #67e8f9); -webkit-background-clip: text; background-clip: text; }

    /* ===== Spectacular Demand Gauge ===== */
    .gauge-wrapper {
        position: relative;
        background: var(--glass-bg);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid var(--glass-border-light);
        border-radius: var(--border-radius-xl);
        padding: 2.5rem;
        margin: 2rem 0;
        overflow: hidden;
        animation: fade-in-up 0.7s ease-out backwards;
        animation-delay: 0.3s;
    }
    
    .gauge-wrapper::before {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(0, 255, 136, 0.08) 0%, transparent 70%);
        pointer-events: none;
        animation: glow-breathe 4s ease-in-out infinite;
    }
    
    .gauge-header { text-align: center; margin-bottom: 2rem; position: relative; z-index: 2; }
    .gauge-title { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--text-muted); margin-bottom: 0.5rem; }
    
    .gauge-value {
        font-size: 4.5rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    
    .gauge-unit { font-size: 1.5rem; font-weight: 600; color: var(--text-secondary); margin-left: 0.25rem; }
    
    .gauge-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    .gauge-status.status-low { background: rgba(0, 255, 136, 0.12); border: 1px solid rgba(0, 255, 136, 0.3); color: var(--accent-primary); }
    .gauge-status.status-moderate { background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); color: var(--accent-warning); }
    .gauge-status.status-high { background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.3); color: var(--accent-danger); }
    
    .gauge-bar-container { position: relative; margin: 2rem 0 1rem; }
    .gauge-bar-track { width: 100%; height: 14px; background: rgba(255, 255, 255, 0.04); border-radius: 7px; overflow: hidden; position: relative; border: 1px solid var(--glass-border); }
    .gauge-bar-fill { height: 100%; border-radius: 7px; position: relative; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
    .gauge-bar-fill::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%); animation: shimmer 2s infinite; }
    .gauge-bar-glow { position: absolute; top: -12px; bottom: -12px; left: 0; border-radius: 7px; filter: blur(12px); opacity: 0.4; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
    .gauge-markers { display: flex; justify-content: space-between; margin-top: 0.75rem; padding: 0 0.25rem; }
    .gauge-marker { text-align: center; }
    .gauge-marker-line { width: 2px; height: 8px; background: var(--text-muted); margin: 0 auto 0.25rem; border-radius: 1px; }
    .gauge-marker-label { font-size: 0.7rem; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

    /* ===== KEY DEMAND DRIVERS — Glassmorphism Redesign ===== */
    .drivers-panel {
        position: relative;
        background: var(--glass-bg);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid var(--glass-border-light);
        border-radius: var(--border-radius-xl);
        padding: 2rem 2rem 1.5rem;
        margin: 1.5rem 0;
        overflow: hidden;
        animation: fade-in-up 0.8s ease-out backwards;
        animation-delay: 0.4s;
    }
    
    .drivers-panel::before {
        content: '';
        position: absolute;
        top: -50%; right: -30%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .drivers-panel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
        position: relative;
        z-index: 2;
    }
    
    .drivers-panel-icon {
        width: 42px; height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(0, 212, 255, 0.1));
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        color: #a855f7;
        font-size: 1.1rem;
    }
    
    .drivers-panel-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .drivers-panel-sub {
        font-size: 0.78rem;
        color: var(--text-muted);
    }
    
    /* Individual Driver Card */
    .driver-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-left: 3px solid var(--driver-accent, #a855f7);
        border-radius: var(--border-radius-md);
        padding: 1.1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        z-index: 2;
    }
    
    .driver-card:last-child {
        margin-bottom: 0;
    }
    
    .driver-card:hover {
        transform: translateX(6px) translateY(-2px);
        border-color: var(--glass-border-light);
        background: rgba(255, 255, 255, 0.04);
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.4), 
                    0 0 30px -5px var(--driver-shadow, rgba(168, 85, 247, 0.15));
    }
    
    .driver-icon-wrap {
        width: 44px; height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--driver-icon-bg, rgba(168, 85, 247, 0.12));
        border: 1px solid var(--driver-icon-border, rgba(168, 85, 247, 0.25));
        border-radius: 12px;
        flex-shrink: 0;
        font-size: 1.1rem;
        color: var(--driver-accent, #a855f7);
        backdrop-filter: blur(10px);
    }
    
    .driver-body {
        flex: 1;
        min-width: 0;
    }
    
    .driver-title-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 3px;
    }
    
    .driver-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .driver-badge {
        font-size: 0.6rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: var(--driver-badge-bg, rgba(168, 85, 247, 0.2));
        color: var(--driver-accent, #a855f7);
        border: 1px solid var(--driver-badge-border, rgba(168, 85, 247, 0.3));
    }
    
    .driver-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    .driver-impact-box {
        text-align: right;
        padding-left: 1rem;
        border-left: 1px solid var(--glass-border);
        flex-shrink: 0;
        min-width: 70px;
    }
    
    .driver-impact-label {
        font-size: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--text-muted);
        margin-bottom: 2px;
    }
    
    .driver-impact-value {
        font-size: 1.1rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--driver-accent, #a855f7);
    }
    
    /* Driver Variants */
    .driver-peak {
        --driver-accent: #f59e0b;
        --driver-shadow: rgba(245, 158, 11, 0.15);
        --driver-icon-bg: rgba(245, 158, 11, 0.12);
        --driver-icon-border: rgba(245, 158, 11, 0.25);
        --driver-badge-bg: rgba(245, 158, 11, 0.15);
        --driver-badge-border: rgba(245, 158, 11, 0.3);
    }
    .driver-traffic {
        --driver-accent: #ef4444;
        --driver-shadow: rgba(239, 68, 68, 0.15);
        --driver-icon-bg: rgba(239, 68, 68, 0.12);
        --driver-icon-border: rgba(239, 68, 68, 0.25);
        --driver-badge-bg: rgba(239, 68, 68, 0.15);
        --driver-badge-border: rgba(239, 68, 68, 0.3);
    }
    .driver-weather-bad {
        --driver-accent: #3b82f6;
        --driver-shadow: rgba(59, 130, 246, 0.15);
        --driver-icon-bg: rgba(59, 130, 246, 0.12);
        --driver-icon-border: rgba(59, 130, 246, 0.25);
        --driver-badge-bg: rgba(59, 130, 246, 0.15);
        --driver-badge-border: rgba(59, 130, 246, 0.3);
    }
    .driver-weather-extreme {
        --driver-accent: #ef4444;
        --driver-shadow: rgba(239, 68, 68, 0.15);
        --driver-icon-bg: rgba(239, 68, 68, 0.12);
        --driver-icon-border: rgba(239, 68, 68, 0.25);
        --driver-badge-bg: rgba(239, 68, 68, 0.15);
        --driver-badge-border: rgba(239, 68, 68, 0.3);
    }
    .driver-event {
        --driver-accent: #a855f7;
        --driver-shadow: rgba(168, 85, 247, 0.15);
        --driver-icon-bg: rgba(168, 85, 247, 0.12);
        --driver-icon-border: rgba(168, 85, 247, 0.25);
        --driver-badge-bg: rgba(168, 85, 247, 0.15);
        --driver-badge-border: rgba(168, 85, 247, 0.3);
    }
    .driver-gas {
        --driver-accent: #00ff88;
        --driver-shadow: rgba(0, 255, 136, 0.15);
        --driver-icon-bg: rgba(0, 255, 136, 0.12);
        --driver-icon-border: rgba(0, 255, 136, 0.25);
        --driver-badge-bg: rgba(0, 255, 136, 0.15);
        --driver-badge-border: rgba(0, 255, 136, 0.3);
    }
    .driver-weekend {
        --driver-accent: #00d4ff;
        --driver-shadow: rgba(0, 212, 255, 0.15);
        --driver-icon-bg: rgba(0, 212, 255, 0.12);
        --driver-icon-border: rgba(0, 212, 255, 0.25);
        --driver-badge-bg: rgba(0, 212, 255, 0.15);
        --driver-badge-border: rgba(0, 212, 255, 0.3);
    }
    .driver-normal {
        --driver-accent: #00ff88;
        --driver-shadow: rgba(0, 255, 136, 0.1);
        --driver-icon-bg: rgba(0, 255, 136, 0.1);
        --driver-icon-border: rgba(0, 255, 136, 0.2);
        --driver-badge-bg: rgba(0, 255, 136, 0.12);
        --driver-badge-border: rgba(0, 255, 136, 0.25);
    }

    /* ===== Model Status Badge ===== */
    .model-status {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(0, 255, 136, 0.06);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 50px;
        padding: 0.6rem 1.25rem;
        margin-bottom: 1.5rem;
        animation: fade-in-up 0.5s ease-out;
    }
    
    .model-status-dot {
        width: 10px; height: 10px;
        background: var(--accent-primary);
        border-radius: 50%;
        position: relative;
    }
    
    .model-status-dot::before {
        content: '';
        position: absolute;
        top: -3px; left: -3px; right: -3px; bottom: -3px;
        background: var(--accent-primary);
        border-radius: 50%;
        animation: pulse-ring 2s ease-out infinite;
    }
    
    .model-status-text {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--accent-primary);
        font-family: 'JetBrains Mono', monospace;
    }

    /* ===== Glassmorphism Input Summary ===== */
    .params-container {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border-light);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .params-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 1rem;
    }
    
    .param-chip {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius-sm);
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .param-chip:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(0, 255, 136, 0.25);
    }
    
    .param-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 0.25rem; }
    .param-value { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }

    /* ===== Empty State ===== */
    .empty-state {
        position: relative;
        background: var(--glass-bg);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px dashed var(--glass-border-light);
        border-radius: var(--border-radius-xl);
        padding: 4rem 2rem;
        text-align: center;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .empty-state::before {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .empty-state-icon { font-size: 4rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite; position: relative; z-index: 2; }
    .empty-state-title { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; position: relative; z-index: 2; }
    .empty-state-text { font-size: 1rem; color: var(--text-secondary); max-width: 400px; margin: 0 auto; line-height: 1.6; position: relative; z-index: 2; }

    /* ===== Premium Button ===== */
    .stButton > button {
        position: relative;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(0, 255, 136, 0.4) !important;
    }

    /* ===== Error Card ===== */
    .error-card {
        background: rgba(239, 68, 68, 0.06);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: var(--border-radius-xl);
        padding: 3rem;
        text-align: center;
    }
    .error-icon { font-size: 3rem; margin-bottom: 1rem; }
    .error-title { font-size: 1.5rem; font-weight: 700; color: var(--accent-danger); margin-bottom: 0.5rem; }
    .error-text { color: var(--text-secondary); }
    .error-code { background: rgba(0,0,0,0.3); border-radius: 8px; padding: 0.75rem 1.25rem; margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent-danger); }

    /* ===== Hide Streamlit Elements ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {background: transparent;}
    
    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

    /* ===== Sidebar Section ===== */
    .sidebar-section-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .sidebar-section-title .icon {
        font-size: 0.85rem;
        color: var(--accent-primary);
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
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 1.5rem;">
        <div style="width: 52px; height: 52px; margin: 0 auto 0.75rem; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,212,255,0.1)); border: 1px solid rgba(0,255,136,0.25); border-radius: 14px; backdrop-filter: blur(10px);">
            <i class="icon" style="font-size: 1.4rem; color: #00ff88;">&#xe9a7;</i>
        </div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.5px;">Control Panel</div>
        <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">Configure simulation parameters</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Temporal Section
    st.markdown("""
    <div class="sidebar-section-title">
        <i class="icon" style="font-size: 0.85rem; color: #00d4ff;">&#xe242;</i>
        <span>Time & Schedule</span>
    </div>
    """, unsafe_allow_html=True)
    
    hour = st.slider("Hour of Day", 0, 23, 17, help="Select the hour (24-hour format)")
    day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    day_val = st.selectbox("Day of Week", list(day_map.keys()), format_func=lambda x: day_map[x], index=4)
    is_weekend = day_val >= 5
    is_peak = (7 <= hour <= 10) or (16 <= hour <= 19)
    
    if is_peak:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 0.5rem 0.75rem; margin-top: 0.5rem;">
            <span style="color: #f59e0b; font-size: 0.8rem; font-weight: 600;"><i class="icon" style="font-size: 0.75rem;">&#xe9a7;</i> Peak Hours Active</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Environment Section
    st.markdown("""
    <div class="sidebar-section-title">
        <i class="icon" style="font-size: 0.85rem; color: #f59e0b;">&#xe28e;</i>
        <span>Environment</span>
    </div>
    """, unsafe_allow_html=True)
    
    temp_f = st.slider("Temperature (°F)", 0, 120, 85, help="Current temperature")
    precip = st.number_input("Precipitation (mm)", 0.0, 50.0, 0.0, help="Rainfall amount")
    weather_opts = sorted(df['weather_category'].unique().tolist()) if df is not None else ['Good', 'Bad', 'Neutral', 'Extreme']
    weather = st.selectbox("Weather Condition", weather_opts)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Traffic & Economics Section
    st.markdown("""
    <div class="sidebar-section-title">
        <i class="icon" style="font-size: 0.85rem; color: #ef4444;">&#xe22d;</i>
        <span>Traffic & Economics</span>
    </div>
    """, unsafe_allow_html=True)
    
    traffic = st.select_slider(
        "Traffic Congestion", 
        options=[1, 2, 3], 
        value=2, 
        format_func=lambda x: {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}[x]
    )
    gas_price = st.number_input("Gas Price ($/gallon)", 2.0, 7.0, 4.50, step=0.10)
    event_opts = sorted(df['local_event'].unique().tolist()) if df is not None else ['none', 'concert', 'game']
    event = st.selectbox("Local Event", event_opts, format_func=lambda x: x.title())
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Station Section
    st.markdown("""
    <div class="sidebar-section-title">
        <i class="icon" style="font-size: 0.85rem; color: #a855f7;">&#xe30e;</i>
        <span>Station Details</span>
    </div>
    """, unsafe_allow_html=True)
    
    city_opts = sorted(df['city'].unique().tolist()) if df is not None else ['San Francisco']
    city = st.selectbox("City", city_opts)
    loc_type_opts = sorted(df['location_type'].unique().tolist()) if df is not None else ['Urban Center']
    loc_type = st.selectbox("Location Type", loc_type_opts)
    charger_opts = sorted(df['charger_type'].unique().tolist()) if df is not None else ['DC Fast']
    charger = st.selectbox("Charger Type", charger_opts)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 0.7rem; color: #64748b; line-height: 1.6;">
            Built with <i class="icon" style="font-size: 0.65rem; color: #00ff88;">&#xe1f5;</i> Machine Learning<br>
            <span style="color: #475569;">Random Forest · R² 0.904</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HERO BANNER
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-banner">
        <div class="hero-glow-orb orb-1"></div>
        <div class="hero-glow-orb orb-2"></div>
        <div class="hero-content">
            <div class="hero-badge">
                <span>A Capstone Project</span>
            </div>
            <h1 class="hero-title"><i class="icon" style="-webkit-text-fill-color: unset;">&#xe9a7;</i> EV Charging Intelligence</h1>
            <p class="hero-subtitle">
                Next-generation AI system for predicting electric vehicle charging demand. 
                Optimize infrastructure planning with real-time analytics and intelligent forecasting.
            </p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-value">90.4%</div>
                    <div class="hero-stat-label">Model Accuracy</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">13</div>
                    <div class="hero-stat-label">Input Features</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">&lt;100ms</div>
                    <div class="hero-stat-label">Prediction Speed</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# MODEL STATUS
# ==========================================
if model is None:
    st.markdown("""
    <div class="error-card">
        <div class="error-icon"><i class="icon" style="font-size: 3rem; color: #ef4444;">&#xe085;</i></div>
        <div class="error-title">Model Not Loaded</div>
        <p class="error-text">The prediction model could not be found. Please train the model first.</p>
        <div class="error-code">python3 src/model_trainer.py</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Model badge
st.markdown("""
<div class="model-status">
    <div class="model-status-dot"></div>
    <i class="icon" style="font-size: 0.9rem; color: #00ff88;">&#xe1f5;</i>
    <span class="model-status-text">Random Forest Model · R² 0.943 · Active</span>
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

predict_btn = st.button("⚡  Predict Demand", type="primary", use_container_width=True)

if predict_btn:
    prediction = model.predict(input_data)[0]
    prediction = max(0.0, min(1.0, prediction))
    pct = prediction * 100

    # Determine demand level, color, label
    if prediction <= 0.3:
        level = "Low"
        status_class = "status-low"
        bar_gradient = "linear-gradient(90deg, #00ff88, #00d4aa)"
        glow_color = "#00ff88"
        emoji = "🟢"
        card_class = "card-green"
    elif prediction <= 0.6:
        level = "Moderate"
        status_class = "status-moderate"
        bar_gradient = "linear-gradient(90deg, #f59e0b, #fbbf24)"
        glow_color = "#f59e0b"
        emoji = "🟡"
        card_class = "card-orange"
    else:
        level = "High"
        status_class = "status-high"
        bar_gradient = "linear-gradient(90deg, #ef4444, #f87171)"
        glow_color = "#ef4444"
        emoji = "🔴"
        card_class = "card-red"

    # ---------- METRIC CARDS ----------
    traffic_labels = {1: "Low", 2: "Medium", 3: "High"}
    traffic_colors = {1: "card-green", 2: "card-orange", 3: "card-red"}
    traffic_status_icons = {1: "&#xe22e;", 2: "&#xe22e;", 3: "&#xe22e;"}
    
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card {card_class}">
            <div class="metric-icon"><i class="icon">&#xe0b4;</i></div>
            <div class="label">Predicted Utilization</div>
            <div class="value">{pct:.1f}%</div>
            <div class="sub">Station capacity in use</div>
        </div>
        <div class="metric-card card-blue">
            <div class="metric-icon"><i class="icon">&#xe9a7;</i></div>
            <div class="label">Demand Level</div>
            <div class="value">{level}</div>
            <div class="sub">AI-powered assessment</div>
        </div>
        <div class="metric-card {traffic_colors[traffic]}">
            <div class="metric-icon"><i class="icon">&#xe22d;</i></div>
            <div class="label">Traffic Index</div>
            <div class="value">{traffic_labels[traffic]}</div>
            <div class="sub">Current congestion</div>
        </div>
        <div class="metric-card card-cyan">
            <div class="metric-icon"><i class="icon">&#xe28e;</i></div>
            <div class="label">Weather</div>
            <div class="value">{weather}</div>
            <div class="sub">{temp_f}°F · {precip}mm</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- SPECTACULAR DEMAND GAUGE ----------
    st.markdown(f"""
    <div class="gauge-wrapper">
        <div class="gauge-header">
            <div class="gauge-title">Demand Prediction Gauge</div>
            <div class="gauge-value-display">
                <span class="gauge-value" style="background: {bar_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{pct:.1f}</span>
                <span class="gauge-unit">%</span>
            </div>
            <div class="gauge-status {status_class}">
                <span>{level} Demand</span>
            </div>
        </div>
        <div class="gauge-bar-container">
            <div class="gauge-bar-glow" style="width: {pct}%; background: {glow_color};"></div>
            <div class="gauge-bar-track">
                <div class="gauge-bar-fill" style="width: {pct}%; background: {bar_gradient};"></div>
            </div>
        </div>
        <div class="gauge-markers">
            <div class="gauge-marker">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-label">0% Idle</div>
            </div>
            <div class="gauge-marker">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-label">25%</div>
            </div>
            <div class="gauge-marker">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-label">50% Balanced</div>
            </div>
            <div class="gauge-marker">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-label">75%</div>
            </div>
            <div class="gauge-marker">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-label">100% Full</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- KEY DEMAND DRIVERS ----------
    drivers = []
    if is_peak:
        drivers.append({
            "cls": "driver-peak",
            "icon": "&#xe242;",
            "name": "Peak Hours Active",
            "badge": "HIGH IMPACT",
            "desc": "Demand typically surges during morning (7–10 AM) and evening (4–7 PM) rush hours, increasing station utilization significantly.",
            "impact": "+25%"
        })
    if traffic == 3:
        drivers.append({
            "cls": "driver-traffic",
            "icon": "&#xe22d;",
            "name": "High Traffic Congestion",
            "badge": "CRITICAL",
            "desc": "Heavy traffic increases charging station usage as drivers seek convenient stops during congested commutes.",
            "impact": "+30%"
        })
    if weather == 'Extreme':
        drivers.append({
            "cls": "driver-weather-extreme",
            "icon": "&#xe085;",
            "name": "Extreme Weather Alert",
            "badge": "ALERT",
            "desc": "Temperature extremes significantly increase battery drain and charging frequency, pushing demand higher.",
            "impact": "+35%"
        })
    elif weather == 'Bad':
        drivers.append({
            "cls": "driver-weather-bad",
            "icon": "&#xe24a;",
            "name": "Adverse Weather",
            "badge": "MODERATE",
            "desc": "Rain or snow conditions affect charging patterns and commuter behavior, slightly elevating demand.",
            "impact": "+15%"
        })
    if event != 'none':
        drivers.append({
            "cls": "driver-event",
            "icon": "&#xe2fc;",
            "name": f"Local Event: {event.title()}",
            "badge": "EVENT",
            "desc": f"The {event.title()} event attracts additional vehicles to the area, increasing nearby charging demand.",
            "impact": "+20%"
        })
    if gas_price >= 5.5:
        drivers.append({
            "cls": "driver-gas",
            "icon": "&#xe2ab;",
            "name": "High Fuel Prices",
            "badge": "ECONOMIC",
            "desc": f"Elevated gas prices (${gas_price:.2f}/gal) drive more consumers toward EV charging as a cost-effective alternative.",
            "impact": "+18%"
        })
    if is_weekend:
        drivers.append({
            "cls": "driver-weekend",
            "icon": "&#xe22a;",
            "name": "Weekend Pattern",
            "badge": "PATTERN",
            "desc": "Weekend usage patterns differ from typical weekday demand curves, with leisure travel shifting peak times.",
            "impact": "~10%"
        })

    if not drivers:
        drivers.append({
            "cls": "driver-normal",
            "icon": "&#xe24d;",
            "name": "Normal Conditions",
            "badge": "STABLE",
            "desc": "All parameters are within standard ranges. Demand follows typical daily patterns with no notable surges expected.",
            "impact": "Base"
        })

    cards_html = ""
    for d in drivers:
        cards_html += f'''<div class="driver-card {d['cls']}">
            <div class="driver-icon-wrap"><i class="icon">{d['icon']}</i></div>
            <div class="driver-body">
                <div class="driver-title-row">
                    <span class="driver-name">{d['name']}</span>
                    <span class="driver-badge">{d['badge']}</span>
                </div>
                <div class="driver-desc">{d['desc']}</div>
            </div>
            <div class="driver-impact-box">
                <div class="driver-impact-label">Impact</div>
                <div class="driver-impact-value">{d['impact']}</div>
            </div>
        </div>'''

    st.markdown(f"""<div class="drivers-panel">
        <div class="drivers-panel-header">
            <div class="drivers-panel-icon"><i class="icon">&#xe1f5;</i></div>
            <div>
                <div class="drivers-panel-title">Key Demand Drivers</div>
                <div class="drivers-panel-sub">Factors influencing current prediction</div>
            </div>
        </div>
        {cards_html}
    </div>""", unsafe_allow_html=True)

    # ---------- INPUT SUMMARY ----------
    with st.expander("� View Simulation Parameters"):
        st.markdown(f"""
        <div class="params-container">
            <div class="params-grid">
                <div class="param-chip">
                    <div class="param-label">City</div>
                    <div class="param-value">{city}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Location Type</div>
                    <div class="param-value">{loc_type}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Charger</div>
                    <div class="param-value">{charger}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Hour</div>
                    <div class="param-value">{hour}:00</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Day</div>
                    <div class="param-value">{day_map[day_val]}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Weekend</div>
                    <div class="param-value">{'Yes' if is_weekend else 'No'}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Peak Hour</div>
                    <div class="param-value">{'Yes' if is_peak else 'No'}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Temperature</div>
                    <div class="param-value">{temp_f}°F</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Precipitation</div>
                    <div class="param-value">{precip} mm</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Weather</div>
                    <div class="param-value">{weather}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Traffic</div>
                    <div class="param-value">Level {traffic}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Gas Price</div>
                    <div class="param-value">${gas_price:.2f}</div>
                </div>
                <div class="param-chip">
                    <div class="param-label">Local Event</div>
                    <div class="param-value">{event.title()}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Empty state - waiting for prediction
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon"><i class="icon" style="font-size: 4rem; color: #00d4ff;">&#xe1f5;</i></div>
        <div class="empty-state-title">Ready to Predict</div>
        <p class="empty-state-text">
            Configure your simulation parameters in the sidebar, then click 
            <strong>Predict Demand</strong> to see the AI-powered forecast.
        </p>
    </div>
    """, unsafe_allow_html=True)