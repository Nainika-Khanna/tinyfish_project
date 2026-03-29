import streamlit as st
import pandas as pd

st.title("Startup Funding Intelligence Dashboard")

# Load data safely
try:
    df = pd.read_csv("funding_data_full_dashboard.csv")
    st.success("Data loaded successfully ✅")
    st.write(df.head())

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
