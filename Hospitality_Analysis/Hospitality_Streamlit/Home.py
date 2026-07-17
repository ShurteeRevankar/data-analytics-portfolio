# ==========================================================
# HOME PAGE
# Hospitality Analytics Dashboard
# ==========================================================

import streamlit as st
import pandas as pd

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Hospitality Analytics Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_hospitality_dataset.csv")

df = load_data()

# ----------------------------------------------------------
# Title
# ----------------------------------------------------------

st.title("🏨 Hospitality Analytics Dashboard")

st.markdown("""
### Data Analytics Internship Project

Analyze hotel bookings, revenue, customer ratings, and predict booking status using Machine Learning.
""")

st.divider()

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

total_revenue = df["revenue_realized"].sum()
total_bookings = len(df)
total_properties = df["property_name"].nunique()
total_cities = df["city"].nunique()
avg_rating = df["ratings_given"].mean()
avg_stay = df["Stay_Duration"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")

with col2:
    st.metric("🛎 Total Bookings", f"{total_bookings:,}")

with col3:
    st.metric("🏨 Properties", total_properties)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("🌍 Cities", total_cities)

with col5:
    st.metric("⭐ Average Rating", f"{avg_rating:.2f}")

with col6:
    st.metric("🛏 Avg Stay", f"{avg_stay:.1f} Days")

st.divider()

# ----------------------------------------------------------
# Project Overview
# ----------------------------------------------------------

st.header("📌 Project Overview")

st.write("""
This Hospitality Analytics Dashboard provides insights into hotel booking performance.

### Objectives

- Analyze hotel revenue
- Study booking trends
- Compare property performance
- Analyze customer ratings
- Analyze booking platforms
- Predict Booking Status using Machine Learning

### Technology Used

- Python
- Pandas
- Streamlit
- Plotly
- Scikit-Learn
""")

st.divider()

# ----------------------------------------------------------
# Dataset Information
# ----------------------------------------------------------

st.header("📂 Dataset Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric("Rows", df.shape[0])

with info2:
    st.metric("Columns", df.shape[1])

with info3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

st.write("### Dataset Columns")

st.dataframe(
    pd.DataFrame(df.columns, columns=["Column Name"]),
    use_container_width=True
)

st.divider()

# ----------------------------------------------------------
# Dataset Preview
# ----------------------------------------------------------

st.header("🔍 Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ----------------------------------------------------------
# Quick Summary
# ----------------------------------------------------------

st.header("📊 Quick Summary")

summary = pd.DataFrame({
    "Metric": [
        "Revenue",
        "Bookings",
        "Properties",
        "Cities",
        "Average Rating",
        "Average Stay Duration"
    ],
    "Value": [
        f"₹ {total_revenue:,.0f}",
        total_bookings,
        total_properties,
        total_cities,
        round(avg_rating,2),
        round(avg_stay,2)
    ]
})

st.dataframe(summary, use_container_width=True)

st.divider()

# ----------------------------------------------------------
# Navigation
# ----------------------------------------------------------

st.header("📁 Dashboard Pages")

st.success("""
Use the left sidebar to explore the dashboard.

🏠 Home

📊 Executive Overview

🏨 Property Performance

🤖 Booking Status Prediction
""")

st.divider()

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

st.caption("Hospitality Analytics Dashboard | ReadyNest Internship Project")