import streamlit as st
import pandas as pd
import time

from db import alerts_collection

# App page config
st.set_page_config(layout="wide")
st.title("Login Alerts System")

# Download alerts from db
alerts = list(alerts_collection.find().sort("timestamp", -1))

if alerts:
    df = pd.DataFrame(alerts)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df = df.drop(columns=["_id"])
    
    alert_type = st.selectbox("Filter by alert type", ["All"] + df["type"].unique().tolist())

    if alert_type != "All":
        df = df[df["type"] == alert_type]
    
    df = df.rename(columns={
        "type": "Alert Type", 
        "ip_address": "IP Address", 
        "timestamp": "Time", "from": 
        "Previous Location", "to": 
        "Current Location", 
        "dominant_device": "Dominant Device", 
        "used_device": "Used Device", 
        "dominance_ratio": "Dominance Ratio", 
        "attempts": "Attempts"
        })
    
    st.dataframe(df.dropna(axis=1, how="all"))
else:
    st.info("No alerts in the database.")
    

if st.button("Refresh now"):
    st.rerun()

# streamlit run streamlit_app.py
