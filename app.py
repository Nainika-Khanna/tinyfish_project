import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Startup Dashboard", layout="wide")

st.title(" Startup Funding Intelligence Dashboard")

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

# ---------- SIDEBAR ----------
st.sidebar.header(" Filters")

year = st.sidebar.multiselect("Year", sorted(df["year"].dropna().unique()))
if year:
    df = df[df["year"].isin(year)]

round_type = st.sidebar.multiselect("Funding Round", df["round"].dropna().unique())
if round_type:
    df = df[df["round"].isin(round_type)]

# ---------- CLASSIFICATION ----------
q1 = df["funding_amount_numeric"].quantile(0.25)
q3 = df["funding_amount_numeric"].quantile(0.75)

def classify(x):
    if x >= q3:
        return "Top "
    elif x <= q1:
        return "Low "
    else:
        return "Moderate"

df["category"] = df["funding_amount_numeric"].apply(classify)

# ---------- KPIs ----------
st.subheader(" Key Insights")

col1, col2, col3, col4 = st.columns(4)

total_funding = df["funding_amount_numeric"].sum()
avg_funding = df["funding_amount_numeric"].mean()
max_funding = df["funding_amount_numeric"].max()
min_funding = df["funding_amount_numeric"].min()

col1.metric(" Total Funding", f"${total_funding:,.0f}M")
col2.metric(" Avg Funding", f"${avg_funding:,.2f}M")
col3.metric(" Highest Funding", f"${max_funding}M")
col4.metric(" Lowest Funding", f"${min_funding}M")

# ---------- TOP FUNDING ----------
st.subheader(" Top 10 Startups by Funding")

top_df = df.sort_values("funding_amount_numeric", ascending=False).head(10)

fig1 = px.bar(
    top_df,
    x="startup_name",
    y="funding_amount_numeric",
    color="category",
    text=top_df["funding_amount_numeric"].apply(lambda x: f"${x}M"),
    color_discrete_map={
        "Top ": "#A8E6CF",
        "Moderate": "#A0C4FF",
        "Low ": "#FFADAD"
    }
)

fig1.update_traces(textposition="outside", textfont=dict(size=14, color="black"))

fig1.update_layout(
    xaxis_title="Startup Name",
    yaxis_title="Funding ($M)",
    showlegend=True
)

st.plotly_chart(fig1, use_container_width=True)

# ---------- PIE ----------
st.subheader(" Funding by Round")

round_df = df.groupby("round")["funding_amount_numeric"].sum().reset_index()

fig2 = px.pie(
    round_df,
    names="round",
    values="funding_amount_numeric",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- LINE ----------
st.subheader(" Quarter-wise Trend")

q_df = df.groupby("quarter")["funding_amount_numeric"].sum().reset_index()

fig3 = px.line(
    q_df,
    x="quarter",
    y="funding_amount_numeric",
    markers=True
)

fig3.update_layout(
    xaxis_title="Quarter",
    yaxis_title="Funding ($M)"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- INVESTORS ----------
st.subheader(" Investor Distribution")

inv_df = df["investors"].fillna("Unknown").value_counts().reset_index()
inv_df.columns = ["investor", "count"]

fig4 = px.bar(
    inv_df.head(10),
    x="investor",
    y="count",
    text="count",
    color="count",
    color_continuous_scale="Peach"
)

fig4.update_traces(textposition="outside")

st.plotly_chart(fig4, use_container_width=True)

# ---------- OUTLIERS ----------
st.subheader(" Outliers Detection")

mean = df["funding_amount_numeric"].mean()
std = df["funding_amount_numeric"].std()

df["outlier"] = df["funding_amount_numeric"].apply(
    lambda x: "Outlier " if abs(x - mean) > 2*std else "Normal"
)

fig5 = px.scatter(
    df,
    x="startup_name",
    y="funding_amount_numeric",
    color="outlier",
    size="funding_amount_numeric",
    color_discrete_map={
        "Outlier ": "#FF6B6B",
        "Normal": "#4ECDC4"
    }
)

fig5.update_layout(
    xaxis_title="Startup",
    yaxis_title="Funding ($M)"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------- TABLE HIGHLIGHT ----------
st.subheader(" Data Table (Highlighted)")

def highlight(row):
    if row["category"] == "Top ":
        return ["background-color: #C7F9CC"] * len(row)
    elif row["category"] == "Low ":
        return ["background-color: #FFCCD5"] * len(row)
    else:
        return [""] * len(row)

st.dataframe(df.style.apply(highlight, axis=1))
