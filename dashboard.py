import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="E-Commerce Marketing ROI", layout="wide")

st.title("📊 E-Commerce Marketing Performance & ROAS Dashboard")
st.markdown("Powered by **DuckDB** and **dbt** | Real-time Executive Insights")

# ⚡ Added ttl=10 (cache clears every 10s) so it automatically picks up Airflow updates!
@st.cache_data(ttl=10)
def load_data():
    # ⚡ Added read_only=True so Airflow won't crash when running tasks simultaneously
    conn = duckdb.connect("analytics.duckdb", read_only=True)
    df = conn.execute("SELECT * FROM fct_daily_marketing_performance").df()
    conn.close()

    # FIX 1: Convert metric_date to datetime format and sort chronologically
    df["metric_date"] = pd.to_datetime(df["metric_date"])
    df = df.sort_values("metric_date")
    return df


df = load_data()

# Top KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Net Revenue", f"${df['total_net_revenue'].sum():,.2f}")
col2.metric("Total Ad Spend", f"${df['total_spend'].sum():,.2f}")
col3.metric("Total Orders", f"{df['total_orders'].sum():,}")
avg_roas = round(
    df["total_net_revenue"].sum() / max(df["total_spend"].sum(), 1), 2
)
col4.metric("Blended ROAS", f"{avg_roas}x")

st.divider()

# Channel Filter
channels = ["All Channels"] + list(df["channel"].unique())
selected_channel = st.selectbox("🎯 Select Channel to View Trends:", channels)

if selected_channel == "All Channels":
    chart_df = (
        df.groupby("metric_date")[["total_net_revenue", "total_spend"]]
        .sum()
        .reset_index()
    )
    chart_title = "Daily Revenue vs. Ad Spend (All Channels)"
else:
    chart_df = df[df["channel"] == selected_channel]
    chart_title = f"Daily Revenue vs. Ad Spend — {selected_channel}"

# FIX 2: Added markers=True so individual dots are visible on dates
fig_spend_rev = px.line(
    chart_df,
    x="metric_date",
    y=["total_net_revenue", "total_spend"],
    title=chart_title,
    markers=True,  # Shows dots at every data point
    labels={"value": "Amount ($)", "metric_date": "Date", "variable": "Metric"},
)

st.plotly_chart(fig_spend_rev, use_container_width=True)

# ROAS Bar Chart
fig_roas = px.bar(
    df,
    x="channel",
    y="roas",
    title="Average Return on Ad Spend (ROAS) by Channel",
    color="channel",
)
st.plotly_chart(fig_roas, use_container_width=True)