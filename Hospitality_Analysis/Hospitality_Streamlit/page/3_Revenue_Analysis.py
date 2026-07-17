# ==========================================================
# REVENUE ANALYSIS
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------

st.set_page_config(
    page_title="Revenue Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Revenue Analysis Dashboard")

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\ReadyNest_Internship\Week 5\Week5\data\cleaned_hospitality_dataset.csv")
    df["check_in_date"] = pd.to_datetime(df["check_in_date"])
    return df

df = load_data()

# ----------------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------------

st.sidebar.header("Filters")

selected_city = st.sidebar.multiselect(
    "City",
    sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

selected_month = st.sidebar.multiselect(
    "Month",
    sorted(df["Booking_Month"].unique()),
    default=sorted(df["Booking_Month"].unique())
)

filtered_df = df[
    (df["city"].isin(selected_city)) &
    (df["Booking_Month"].isin(selected_month))
]

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

total_revenue = filtered_df["revenue_realized"].sum()
avg_revenue = filtered_df["revenue_realized"].mean()
max_revenue = filtered_df["revenue_realized"].max()
total_bookings = filtered_df["booking_id"].count()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")
col2.metric("📈 Avg Revenue", f"₹ {avg_revenue:,.0f}")
col3.metric("🏆 Highest Booking Revenue", f"₹ {max_revenue:,.0f}")
col4.metric("🛎 Total Bookings", total_bookings)

st.divider()

# ----------------------------------------------------------
# Revenue Trend
# ----------------------------------------------------------

st.subheader("📅 Revenue Trend")

trend = (
    filtered_df.groupby("check_in_date")["revenue_realized"]
    .sum()
    .reset_index()
)

fig = px.line(
    trend,
    x="check_in_date",
    y="revenue_realized",
    markers=True,
    title="Daily Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue by City
# ----------------------------------------------------------

st.subheader("🌍 Revenue by City")

city = (
    filtered_df.groupby("city")["revenue_realized"]
    .sum()
    .reset_index()
)

fig = px.bar(
    city,
    x="city",
    y="revenue_realized",
    color="city",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue by Property
# ----------------------------------------------------------

st.subheader("🏨 Revenue by Property")

property_df = (
    filtered_df.groupby("property_name")["revenue_realized"]
    .sum()
    .reset_index()
    .sort_values("revenue_realized", ascending=False)
)

fig = px.bar(
    property_df,
    x="property_name",
    y="revenue_realized",
    color="property_name",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue by Room Class
# ----------------------------------------------------------

st.subheader("🛏 Revenue by Room Class")

room = (
    filtered_df.groupby("room_class")["revenue_realized"]
    .sum()
    .reset_index()
)

fig = px.pie(
    room,
    names="room_class",
    values="revenue_realized",
    hole=0.45
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue by Booking Platform
# ----------------------------------------------------------

st.subheader("📱 Revenue by Booking Platform")

platform = (
    filtered_df.groupby("booking_platform")["revenue_realized"]
    .sum()
    .reset_index()
)

fig = px.bar(
    platform,
    x="booking_platform",
    y="revenue_realized",
    color="booking_platform",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue Summary Table
# ----------------------------------------------------------

st.subheader("📋 Revenue Summary")

summary = (
    filtered_df.groupby("property_name")
    .agg(
        Total_Revenue=("revenue_realized", "sum"),
        Total_Bookings=("booking_id", "count"),
        Avg_Revenue=("revenue_realized", "mean")
    )
    .reset_index()
)

summary["Total_Revenue"] = summary["Total_Revenue"].round(0)
summary["Avg_Revenue"] = summary["Avg_Revenue"].round(0)

st.dataframe(summary, use_container_width=True)

st.markdown("---")
st.caption("Hospitality Analytics Dashboard | Revenue Analysis")