# ==========================================================
# HOSPITALITY ANALYTICS
# STEP 3 - MACHINE LEARNING MODEL
# Booking Status Prediction
# ==========================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

print("=" * 70)
print("HOSPITALITY ANALYTICS - MODEL TRAINING")
print("=" * 70)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv(r"D:\ReadyNest_Internship\Week 5\Week5\data\cleaned_hospitality_dataset.csv")

print("\nDataset Shape :", df.shape)

# ----------------------------------------------------------
# Select Features
# ----------------------------------------------------------

features = [
    "city",
    "room_class",
    "booking_platform",
    "no_guests",
    "month",
    "ratings_given"
]

target = "booking_status"

data = df[features + [target]].copy()

# ----------------------------------------------------------
# Handle Missing Values
# ----------------------------------------------------------

numeric_cols = ["no_guests", "ratings_given"]

for col in numeric_cols:
    data[col] = data[col].fillna(data[col].median())

categorical_cols = [
    "city",
    "room_class",
    "booking_platform"
]

for col in categorical_cols:
    data[col] = data[col].fillna("Unknown")

data = data.dropna(subset=[target])

# ----------------------------------------------------------
# Label Encoding
# ----------------------------------------------------------

encoders = {}

for col in categorical_cols + [target]:
    encoder = LabelEncoder()
    data[col] = encoder.fit_transform(data[col].astype(str))
    encoders[col] = encoder

# ----------------------------------------------------------
# Features & Target
# ----------------------------------------------------------

X = data[features]
y = data[target]

# ----------------------------------------------------------
# Train Test Split
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ----------------------------------------------------------
# Model Training
# ----------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

y_pred = model.predict(X_test)

# ----------------------------------------------------------
# Accuracy
# ----------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy")
print("-" * 40)
print(f"{accuracy:.4f}")

# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

print("\nConfusion Matrix")
print("-" * 40)

cm = confusion_matrix(y_test, y_pred)

print(cm)

# ----------------------------------------------------------
# Classification Report
# ----------------------------------------------------------

print("\nClassification Report")
print("-" * 40)

print(classification_report(y_test, y_pred))

# ----------------------------------------------------------
# Feature Importance
# ----------------------------------------------------------

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance")
print("-" * 40)

print(importance)

# ----------------------------------------------------------
# Save Model
# ----------------------------------------------------------

joblib.dump(model, "booking_status_model.pkl")
joblib.dump(encoders, "label_encoders.pkl")

print("\nModel Saved Successfully!")

print("booking_status_model.pkl")
print("label_encoders.pkl")

print("\nModel Training Completed Successfully!")