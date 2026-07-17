# ==========================================================
# PROPERTY PERFORMANCE
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------

st.set_page_config(
    page_title="Property Performance",
    page_icon="🏨",
    layout="wide"
)

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(r"D:\ReadyNest_Internship\Week 5\Week5\data\cleaned_hospitality_dataset.csv")

df = load_data()

st.title("🏨 Property Performance Dashboard")
st.markdown("---")

# ----------------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------------

st.sidebar.header("Filters")

# City Filter
cities = sorted(df["city"].dropna().unique())
selected_city = st.sidebar.multiselect(
    "Select City",
    cities,
    default=cities
)

filtered_df = df[df["city"].isin(selected_city)]

# Property Filter
properties = sorted(filtered_df["property_name"].dropna().unique())
selected_property = st.sidebar.multiselect(
    "Select Property",
    properties,
    default=properties
)

filtered_df = filtered_df[
    filtered_df["property_name"].isin(selected_property)
]

# Room Class Filter
room_classes = sorted(filtered_df["room_class"].dropna().unique())
selected_room = st.sidebar.multiselect(
    "Room Class",
    room_classes,
    default=room_classes
)

filtered_df = filtered_df[
    filtered_df["room_class"].isin(selected_room)
]

# ----------------------------------------------------------
# KPIs
# ----------------------------------------------------------

total_revenue = filtered_df["revenue_realized"].sum()

total_properties = filtered_df["property_name"].nunique()

avg_rating = filtered_df["ratings_given"].mean()

total_bookings = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Properties", total_properties)
col3.metric("Bookings", total_bookings)
col4.metric("Avg Rating", f"{avg_rating:.2f}")

st.markdown("---")

# ----------------------------------------------------------
# Revenue by Property
# ----------------------------------------------------------

property_revenue = (
    filtered_df.groupby("property_name")["revenue_realized"]
    .sum()
    .reset_index()
    .sort_values("revenue_realized", ascending=False)
)

fig = px.bar(
    property_revenue,
    x="property_name",
    y="revenue_realized",
    color="revenue_realized",
    title="Revenue by Property",
    text_auto=".2s"
)

fig.update_layout(xaxis_title="", yaxis_title="Revenue")

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Room Class Distribution
# ----------------------------------------------------------

room_summary = (
    filtered_df.groupby("room_class")
    .agg(
        Revenue=("revenue_realized", "sum"),
        Bookings=("room_class", "count"),
        Avg_Rating=("ratings_given", "mean")
    )
    .reset_index()
)

fig2 = px.bar(
    room_summary,
    x="room_class",
    y="Revenue",
    color="room_class",
    title="Revenue by Room Class",
    text_auto=".2s"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------------
# Room Class Booking Distribution
# ----------------------------------------------------------

fig3 = px.pie(
    filtered_df,
    names="room_class",
    title="Room Class Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------
# Property Summary Table
# ----------------------------------------------------------

st.subheader("📋 Property Summary")

summary = (
    filtered_df.groupby("property_name")
    .agg(
        City=("city", "first"),
        Revenue=("revenue_realized", "sum"),
        Bookings=("property_name", "count"),
        Avg_Rating=("ratings_given", "mean")
    )
    .reset_index()
)

summary["Revenue"] = summary["Revenue"].round(0)
summary["Avg_Rating"] = summary["Avg_Rating"].round(2)

st.dataframe(summary, use_container_width=True)

# ----------------------------------------------------------
# Top 10 Properties
# ----------------------------------------------------------

st.subheader("🏆 Top 10 Revenue Generating Properties")

top10 = summary.sort_values(
    "Revenue",
    ascending=False
).head(10)

fig4 = px.bar(
    top10,
    x="property_name",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

fig4.update_layout(
    xaxis_title="Property",
    yaxis_title="Revenue"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------------
# Download Summary
# ----------------------------------------------------------

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Property Summary",
    data=csv,
    file_name="property_summary.csv",
    mime="text/csv"
)