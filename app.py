import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

# ---------- CLASSIFICATION ----------
def classify(row):
    q1 = df["funding_amount_numeric"].quantile(0.25)
    q3 = df["funding_amount_numeric"].quantile(0.75)

    if row["funding_amount_numeric"] >= q3:
        return "Top Performer 🚀"
    elif row["funding_amount_numeric"] <= q1:
        return "Low Performer ⚠️"
    else:
        return "Moderate"

df["category"] = df.apply(classify, axis=1)

# ---------- METRICS ----------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Startups", len(df))
col2.metric("Total Funding ($M)", int(df["funding_amount_numeric"].sum()))
col3.metric("Avg Funding ($M)", round(df["funding_amount_numeric"].mean(), 2))

# ---------- TOP FUNDING ----------
st.subheader("📊 Top 10 Funding (Bar Chart)")

top_startups = df.sort_values(by="funding_amount_numeric", ascending=False).head(10)

fig1 = px.bar(
    top_startups,
    x="startup_name",
    y="funding_amount_numeric",
    text="funding_amount_numeric",
    color="category",
    color_discrete_map={
        "Top Performer 🚀": "green",
        "Moderate": "blue",
        "Low Performer ⚠️": "red"
    }
)

fig1.update_traces(textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# ---------- LOW FUNDING ----------
st.subheader("📉 Lowest Funded Startups")

low_startups = df.sort_values(by="funding_amount_numeric").head(10)
st.dataframe(low_startups[["startup_name", "funding_amount", "round"]])

# ---------- PIE CHART ----------
st.subheader("🥧 Funding Distribution by Round")

round_funding = df.groupby("round")["funding_amount_numeric"].sum().reset_index()

fig2 = px.pie(
    round_funding,
    names="round",
    values="funding_amount_numeric",
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- LINE CHART ----------
st.subheader("📈 Quarter-wise Funding Trend")

quarter_data = df.groupby("quarter")["funding_amount_numeric"].sum().reset_index()

fig3 = px.line(
    quarter_data,
    x="quarter",
    y="funding_amount_numeric",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- INVESTOR CHART ----------
st.subheader("💼 Investor Count")

investor_count = df["investors"].fillna("Unknown").value_counts().reset_index()
investor_count.columns = ["investor", "count"]

fig4 = px.bar(
    investor_count.head(10),
    x="investor",
    y="count",
    text="count",
    color="count",
    color_continuous_scale="Oranges"
)

fig4.update_traces(textposition='outside')
st.plotly_chart(fig4, use_container_width=True)

# ---------- OUTLIER DETECTION ----------
st.subheader("🔥 Outlier Detection")

mean = df["funding_amount_numeric"].mean()
std = df["funding_amount_numeric"].std()

df["outlier"] = df["funding_amount_numeric"].apply(
    lambda x: "Outlier 🔥" if abs(x - mean) > 2 * std else "Normal"
)

fig5 = px.scatter(
    df,
    x="startup_name",
    y="funding_amount_numeric",
    color="outlier",
    size="funding_amount_numeric"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------- FULL DATA ----------
st.subheader("📄 Full Data")
st.dataframe(df)
