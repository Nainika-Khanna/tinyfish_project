import streamlit as st
import pandas as pd

st.set_page_config(page_title="Startup Dashboard", layout="wide")

st.title("🚀 Startup Funding Intelligence Dashboard")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("funding_data_full_dashboard.csv")
    df.columns = df.columns.str.strip().str.lower()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)

    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔎 Filters")

year = st.sidebar.multiselect("Year", sorted(df["year"].dropna().unique()))
if year:
    df = df[df["year"].isin(year)]

round_type = st.sidebar.multiselect("Funding Round", df["round"].dropna().unique())
if round_type:
    df = df[df["round"].isin(round_type)]

# ---------- METRICS ----------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Startups", len(df))
col2.metric("Total Funding ($M)", int(df["funding_amount_numeric"].sum()))
col3.metric("Avg Funding ($M)", round(df["funding_amount_numeric"].mean(), 2))

# ---------- TOP FUNDING ----------
st.subheader("🏆 Top Funded Startups")

top_startups = df.sort_values(by="funding_amount_numeric", ascending=False).head(10)
st.dataframe(top_startups[["startup_name", "funding_amount", "round"]])

# ---------- LOW PERFORMERS ----------
st.subheader("📉 Lowest Funded Startups")

low_startups = df.sort_values(by="funding_amount_numeric", ascending=True).head(10)
st.dataframe(low_startups[["startup_name", "funding_amount", "round"]])

# ---------- FUNDING BY ROUND (PIE) ----------
st.subheader("🥧 Funding Distribution by Round")

round_funding = df.groupby("round")["funding_amount_numeric"].sum()
st.plotly_chart({
    "data": [{
        "labels": round_funding.index,
        "values": round_funding.values,
        "type": "pie"
    }]
})

# ---------- QUARTER WISE PERFORMANCE (LINE) ----------
st.subheader("📈 Quarter-wise Funding Trend")

quarter_data = df.groupby("quarter")["funding_amount_numeric"].sum().reset_index()
quarter_data = quarter_data.sort_values("quarter")

st.line_chart(quarter_data.set_index("quarter"))

# ---------- FUNDING BY STARTUP (BAR) ----------
st.subheader("📊 Top 10 Funding (Bar Chart)")

bar_data = top_startups.set_index("startup_name")["funding_amount_numeric"]
st.bar_chart(bar_data)

# ---------- INVESTOR ANALYSIS ----------
st.subheader("💼 Investor Count")

investor_count = df["investors"].fillna("Unknown").value_counts().head(10)
st.bar_chart(investor_count)

# ---------- FULL DATA ----------
st.subheader("📄 Full Data")

st.dataframe(df)
