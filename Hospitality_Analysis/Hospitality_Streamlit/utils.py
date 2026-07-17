# ==========================================================
# HOSPITALITY ANALYTICS - ETL PROCESS
# Step 1: Extract, Transform & Load (ETL)
# ==========================================================

import pandas as pd
import numpy as np

print("="*60)
print("HOSPITALITY ANALYTICS - ETL PROCESS")
print("="*60)

# ----------------------------------------------------------
# 1. Load Dataset
# ----------------------------------------------------------

file_path = "Hospitality_Excel.xlsx"

df = pd.read_excel(file_path)

print("\nDataset Loaded Successfully!")
print("Shape :", df.shape)

# ----------------------------------------------------------
# 2. Basic Information
# ----------------------------------------------------------

print("\nDataset Information")
print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------------------------------------
# 3. Remove Duplicate Records
# ----------------------------------------------------------

duplicate_count = df.duplicated().sum()

print(f"\nDuplicate Rows Found : {duplicate_count}")

df = df.drop_duplicates()

print("Shape After Removing Duplicates :", df.shape)

# ----------------------------------------------------------
# 4. Handle Missing Values
# ----------------------------------------------------------

# Fill numerical columns with median

num_cols = df.select_dtypes(include=['int64','float64']).columns

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Fill categorical columns with mode

cat_cols = df.select_dtypes(include='object').columns

for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("\nMissing Values After Cleaning")
print(df.isnull().sum())

# ----------------------------------------------------------
# 5. Convert Date Columns
# ----------------------------------------------------------

date_columns = []

for col in df.columns:
    if "date" in col.lower():
        date_columns.append(col)

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("\nConverted Date Columns")
print(date_columns)

# ----------------------------------------------------------
# 6. Feature Engineering
# ----------------------------------------------------------

# Month

for col in date_columns:
    df[col + "_Month"] = df[col].dt.month_name()

# Year

for col in date_columns:
    df[col + "_Year"] = df[col].dt.year

# Day

for col in date_columns:
    df[col + "_Day"] = df[col].dt.day

# Stay Duration (if both Check-in & Check-out exist)

possible_checkin = None
possible_checkout = None

for col in df.columns:
    if "check" in col.lower() and "in" in col.lower():
        possible_checkin = col

    if "check" in col.lower() and "out" in col.lower():
        possible_checkout = col

if possible_checkin and possible_checkout:

    df["Stay_Duration"] = (
        df[possible_checkout] - df[possible_checkin]
    ).dt.days

    print("\nStay Duration Feature Created")

# ----------------------------------------------------------
# 7. Final Dataset Information
# ----------------------------------------------------------

print("\nFinal Dataset Shape :", df.shape)

print("\nFirst Five Records")
print(df.head())

# ----------------------------------------------------------
# 8. Save Clean Dataset
# ----------------------------------------------------------

output_file = "cleaned_hospitality_dataset.csv"

df.to_csv(output_file, index=False)

print("\nCleaned Dataset Saved Successfully!")
print("File Name :", output_file)

print("\nETL Completed Successfully!")
print("="*60)