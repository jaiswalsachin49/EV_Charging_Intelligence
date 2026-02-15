# Intelligent EV Charging Demand Prediction & Infrastructure Planning

**Project 15 | Mid-Sem Submission | Milestone 1**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5%2B-orange)

## 📌 Project Overview

This project focuses on building an **AI-driven analytics system** for electric vehicle (EV) infrastructure planning.

In **Milestone 1**, we implement a classical machine learning solution to predict EV charging demand at stations using historical usage data, time, and environmental factors. The goal is to optimize grid load distribution and improve user experience by forecasting utilization rates.

### Key Objectives

- **Predict Demand:** Forecast utilization rates (%) for charging stations.
- **Analyze Drivers:** Identify key factors influencing demand (Time of Day, Traffic, Weather).
- **Visualize Insights:** Provide an interactive dashboard for stakeholders.

## 🚀 Features

- **Data Preprocessing:** Automated cleaning and feature engineering pipeline.
- **ML Model:** Random Forest Regressor optimized for accuracy (R² > 0.90).
- **Interactive UI:** Streamlit-based dashboard with:
  - Real-time demand prediction
  - Dynamic input controls (Time, Weather, Traffic)
  - Visual gauge & metric cards
  - "Key Demand Drivers" insights engine

## 🛠️ Technology Stack

- **Language:** Python 3.12
- **ML Framework:** Scikit-Learn (Pipeline, RandomForestRegressor)
- **Data Processing:** Pandas, NumPy
- **UI Framework:** Streamlit
- **Deployment:** Streamlit Community Cloud (Recommended)

## 📂 Project Structure

```
EV_Charging_Intelligence/
├── data/
│   ├── raw/                # Original dataset
│   └── processed/          # Cleaned data for training
├── models/
│   └── demand_predictor.pkl # Trained model artifact
├── report/
│   ├── system_architecture.mermaid # System diagram
│   └── model_evaluation_report.md  # Detailed metrics
├── src/
│   ├── app.py              # Streamlit dashboard application
│   ├── data_preprocessing.py # EtL script
│   ├── model_trainer_lite.py # Model training script
│   └── evaluate_model.py   # Evaluation metrics script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jaiswalsachin49/EV_Charging_Intelligence.git
   cd EV_Charging_Intelligence
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run src/app.py
   ```

## 📊 Model Performance

The Random Forest model demonstrates strong predictive capability:

- **R-Squared (R²):** 0.9045
- **RMSE:** 0.0926
- **MAE:** 0.0634

_For a detailed analysis, see [Model Evaluation Report](report/model_evaluation_report.md)._

## 🧠 Input/Output Specification

**Inputs:**

- **Temporal:** Hour (0-23), Day of Week
- **Environmental:** Temperature (F), Precipitation (mm), Weather Condition
- **Contextual:** Traffic Index (1-3), Gas Price ($/gal), Local Events
- **Station:** Location Type, Charger Type, City

**Outputs:**

- **Utilization Rate (%):** Predicted percentage of station capacity in use.
- **Demand Level:** Low / Balanced / High / Critical.

## 🔮 Future Work (Milestone 2)

- Transition to **Agentic AI** infrastructure planning.
- Integration with **LangGraph** for autonomous decision making.
- Advanced **RAG** systems for policy and regulation analysis.

---

**Team Members:** Sachin Jaiswal, Ayush Tiwari, Sibtain Ahmed Qureshi, Md. Sajjan
