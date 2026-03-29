# ============================================
# 🚀 STARTUP FUNDING DASHBOARD (STREAMLIT)
# ============================================

# --------------------------------------------
# STEP 1: Import Required Libraries
# --------------------------------------------
import streamlit as st
import pandas as pd

# --------------------------------------------
# STEP 2: Page Configuration
# --------------------------------------------
st.set_page_config(
    page_title="Startup Funding Dashboard",
    layout="wide"
)

# --------------------------------------------
# STEP 3: Title
# --------------------------------------------
st.title("🚀 Startup Funding Intelligence Dashboard")

# --------------------------------------------
# STEP 4: Load Data (CSV file)
# --------------------------------------------
try:
    df = pd.read_csv("funding_data.csv")
    st.success("✅ Data Loaded Successfully")
except Exception as e:
    st.error("❌ Error loading data. Check CSV file.")
    st.stop()

# --------------------------------------------
# STEP 5: Show Top 10 Records (Low Load)
# --------------------------------------------
st.subheader("📊 Top 10 Records")
st.dataframe(df.head(10))

# --------------------------------------------
# STEP 6: Basic Insights (Charts)
# --------------------------------------------

# Show sector distribution (if exists)
if "sector" in df.columns:
    st.subheader("🏭 Top Sectors")
    st.bar_chart(df["sector"].value_counts().head(10))

# Show startup frequency (if exists)
if "startup_name" in df.columns:
    st.subheader("🚀 Top Startups")
    st.bar_chart(df["startup_name"].value_counts().head(10))

# --------------------------------------------
# STEP 7: Search Feature
# --------------------------------------------
st.subheader("🔍 Search Data")

search = st.text_input("Enter keyword:")

if search:
    result = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    st.write(result.head(10))

# --------------------------------------------
# STEP 8: Footer
# --------------------------------------------
st.success("🎯 Dashboard Ready")