# ==========================================================
# HOSPITALITY ANALYTICS
# STEP 2 - EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/cleaned_hospitality_dataset.csv")

print("=" * 60)
print("HOSPITALITY ANALYTICS - EDA")
print("=" * 60)

# ----------------------------------------------------------
# Dataset Overview
# ----------------------------------------------------------

print("\nDataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nSummary Statistics")
print(df.describe())

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------------------------------------
# Revenue by City
# ----------------------------------------------------------

city_revenue = (
    df.groupby("city")["revenue_realized"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by City")
print(city_revenue)

plt.figure(figsize=(8,5))
city_revenue.plot(kind="bar", color="steelblue")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Revenue by Property
# ----------------------------------------------------------

property_revenue = (
    df.groupby("property_name")["revenue_realized"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Property")
print(property_revenue)

plt.figure(figsize=(12,5))
property_revenue.plot(kind="bar", color="orange")
plt.title("Revenue by Property")
plt.xlabel("Property")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Booking Status
# ----------------------------------------------------------

plt.figure(figsize=(6,6))

df["booking_status"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.ylabel("")
plt.title("Booking Status Distribution")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Room Class Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))

sns.countplot(
    data=df,
    x="room_class",
    order=df["room_class"].value_counts().index
)

plt.title("Room Class Distribution")
plt.xlabel("Room Class")
plt.ylabel("Bookings")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Booking Platform
# ----------------------------------------------------------

platform = (
    df.groupby("booking_platform")["revenue_realized"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Booking Platform")
print(platform)

plt.figure(figsize=(10,5))
platform.plot(kind="bar", color="green")
plt.title("Revenue by Booking Platform")
plt.xlabel("Platform")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Ratings Distribution
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sns.histplot(
    df["ratings_given"],
    bins=20,
    kde=True
)

plt.title("Ratings Distribution")
plt.xlabel("Ratings")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Revenue Trend
# ----------------------------------------------------------

df["check_in_date"] = pd.to_datetime(df["check_in_date"])

trend = (
    df.groupby("check_in_date")["revenue_realized"]
    .sum()
)

plt.figure(figsize=(12,5))
trend.plot(color="red")
plt.title("Revenue Trend")
plt.xlabel("Check-in Date")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Revenue by Room Class
# ----------------------------------------------------------

room_revenue = (
    df.groupby("room_class")["revenue_realized"]
    .sum()
)

plt.figure(figsize=(6,4))
room_revenue.plot(kind="bar", color="purple")
plt.title("Revenue by Room Class")
plt.xlabel("Room Class")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Top 10 Revenue Generating Properties
# ----------------------------------------------------------

top10 = property_revenue.head(10)

plt.figure(figsize=(10,5))
top10.plot(kind="bar", color="darkcyan")
plt.title("Top 10 Revenue Generating Properties")
plt.xlabel("Property")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Average Rating by Property
# ----------------------------------------------------------

rating = (
    df.groupby("property_name")["ratings_given"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Rating by Property")
print(rating)

plt.figure(figsize=(10,5))
rating.plot(kind="bar", color="gold")
plt.title("Average Rating by Property")
plt.xlabel("Property")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Average Stay Duration by City
# ----------------------------------------------------------

stay = (
    df.groupby("city")["Stay_Duration"]
    .mean()
)

plt.figure(figsize=(8,5))
stay.plot(kind="bar", color="brown")
plt.title("Average Stay Duration by City")
plt.xlabel("City")
plt.ylabel("Days")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------------

plt.figure(figsize=(8,6))

numeric = df.select_dtypes(include="number")

sns.heatmap(
    numeric.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

print("\nEDA Completed Successfully!")