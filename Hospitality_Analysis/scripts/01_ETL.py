# ==========================================================
# HOSPITALITY ANALYTICS
# STEP 1 - ETL
# ==========================================================

import pandas as pd

print("=" * 60)
print("HOSPITALITY ANALYTICS - ETL")
print("=" * 60)

# ----------------------------------------------------------
# Load Final_Data Sheet
# ----------------------------------------------------------

file_path = "data/Hospitality_Excel.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Final_Data"
)

print("\nOriginal Shape :", df.shape)

# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------

print("\nMissing Values")
print(df.isnull().sum())

# Numeric columns
numeric_cols = df.select_dtypes(include="number").columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Categorical columns
cat_cols = df.select_dtypes(include="object").columns

for col in cat_cols:
    df[col] = df[col].fillna("Unknown")

# ----------------------------------------------------------
# Remove Duplicates
# ----------------------------------------------------------

before = len(df)

df.drop_duplicates(inplace=True)

after = len(df)

print(f"\nDuplicates Removed : {before-after}")

# ----------------------------------------------------------
# Convert Date Columns
# ----------------------------------------------------------

date_cols = [
    "booking_date",
    "check_in_date",
    "checkout_date"
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# ----------------------------------------------------------
# Feature Engineering
# ----------------------------------------------------------

df["Stay_Duration"] = (
    df["checkout_date"] -
    df["check_in_date"]
).dt.days

df["Booking_Month"] = df["check_in_date"].dt.month_name()

df["Booking_Year"] = df["check_in_date"].dt.year

df["Booking_Day"] = df["check_in_date"].dt.day_name()

df["Revenue_Per_Guest"] = (
    df["revenue_realized"] /
    df["no_guests"]
)

# ----------------------------------------------------------
# Save Clean Dataset
# ----------------------------------------------------------

df.to_csv(
    "cleaned_hospitality_dataset.csv",
    index=False
)

print("\nFinal Shape :", df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nDataset saved as cleaned_hospitality_dataset.csv")

print("\nETL Completed Successfully!")