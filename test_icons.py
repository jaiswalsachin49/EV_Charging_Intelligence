import streamlit as st

st.set_page_config(page_title="Test", page_icon=":material/bolt:")

st.title(":material/settings: Control Panel")
st.warning("Peak Hours Active", icon=":material/timer:")

traffic = st.select_slider(
    "Traffic Congestion", 
    options=[1, 2, 3], 
    value=2, 
    format_func=lambda x: {1: ":material/check_circle: Low", 2: ":material/warning: Medium", 3: ":material/error: High"}[x]
)

st.button("Predict Demand", icon=":material/bolt:")

