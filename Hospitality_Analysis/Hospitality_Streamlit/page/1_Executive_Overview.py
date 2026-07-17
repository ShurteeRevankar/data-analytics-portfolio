# ==========================================================
# EXECUTIVE OVERVIEW
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Overview")

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(r"D:\ReadyNest_Internship\Week 5\Week5\data\cleaned_hospitality_dataset.csv")

df = load_data()

# ----------------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------------

st.sidebar.header("Filters")

cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

properties = st.sidebar.multiselect(
    "Select Property",
    options=sorted(df["property_name"].unique()),
    default=sorted(df["property_name"].unique())
)

filtered_df = df[
    (df["city"].isin(cities)) &
    (df["property_name"].isin(properties))
]

# ----------------------------------------------------------
# Revenue KPIs
# ----------------------------------------------------------

total_revenue = filtered_df["revenue_realized"].sum()
total_bookings = len(filtered_df)
avg_rating = filtered_df["ratings_given"].mean()
avg_revenue = filtered_df["revenue_realized"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")
col2.metric("🛎 Total Bookings", f"{total_bookings:,}")
col3.metric("⭐ Average Rating", f"{avg_rating:.2f}")
col4.metric("📈 Avg Revenue", f"₹ {avg_revenue:,.0f}")

st.divider()

# ----------------------------------------------------------
# Revenue by City
# ----------------------------------------------------------

city_revenue = (
    filtered_df
    .groupby("city")["revenue_realized"]
    .sum()
    .reset_index()
)

fig_city = px.bar(
    city_revenue,
    x="city",
    y="revenue_realized",
    color="city",
    title="Revenue by City",
    text_auto=True
)

st.plotly_chart(fig_city, use_container_width=True)

# ----------------------------------------------------------
# Booking Status
# ----------------------------------------------------------

status = (
    filtered_df["booking_status"]
    .value_counts()
    .reset_index()
)

status.columns = ["Booking Status", "Count"]

fig_status = px.pie(
    status,
    names="Booking Status",
    values="Count",
    title="Booking Status Distribution"
)

st.plotly_chart(fig_status, use_container_width=True)

# ----------------------------------------------------------
# Revenue by Booking Platform
# ----------------------------------------------------------

platform = (
    filtered_df
    .groupby("booking_platform")["revenue_realized"]
    .sum()
    .reset_index()
)

fig_platform = px.bar(
    platform,
    x="booking_platform",
    y="revenue_realized",
    color="booking_platform",
    title="Revenue by Booking Platform",
    text_auto=True
)

st.plotly_chart(fig_platform, use_container_width=True)

# ----------------------------------------------------------
# Ratings Distribution
# ----------------------------------------------------------

fig_rating = px.histogram(
    filtered_df,
    x="ratings_given",
    nbins=20,
    title="Ratings Distribution"
)

st.plotly_chart(fig_rating, use_container_width=True)

# ----------------------------------------------------------
# Revenue Summary Table
# ----------------------------------------------------------

st.subheader("Revenue Summary")

summary = (
    filtered_df
    .groupby("city")
    .agg(
        Total_Revenue=("revenue_realized", "sum"),
        Total_Bookings=("booking_id", "count"),
        Average_Rating=("ratings_given", "mean")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)