# ==========================================================
# BOOKING STATUS PREDICTION
# ==========================================================

import streamlit as st
import pandas as pd
import joblib

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Booking Status Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Booking Status Prediction")
st.write("Predict the booking status using the trained Random Forest model.")

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        r"D:\ReadyNest_Internship\Week 5\Week5\data\cleaned_hospitality_dataset.csv"
    )

df = load_data()

# ----------------------------------------------------------
# Load Model
# ----------------------------------------------------------

model = joblib.load(
    r"D:\ReadyNest_Internship\Week 5\Week5\booking_status_model.pkl"
)

encoders = joblib.load(
    r"D:\ReadyNest_Internship\Week 5\Week5\label_encoders.pkl"
)

# ----------------------------------------------------------
# User Inputs
# ----------------------------------------------------------

st.subheader("Booking Details")

col1, col2 = st.columns(2)

with col1:

    city = st.selectbox(
        "City",
        sorted(df["city"].dropna().unique())
    )

    room_class = st.selectbox(
        "Room Class",
        sorted(df["room_class"].dropna().unique())
    )

    booking_platform = st.selectbox(
        "Booking Platform",
        sorted(df["booking_platform"].dropna().unique())
    )

with col2:

    no_guests = st.number_input(
        "Number of Guests",
        min_value=1,
        max_value=10,
        value=2
    )

    month = st.selectbox(
        "Month",
        sorted(df["month"].unique())
    )

    rating = st.slider(
        "Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

if st.button("Predict"):

    try:

        input_data = pd.DataFrame({

            "city": [
                encoders["city"].transform([city])[0]
            ],

            "room_class": [
                encoders["room_class"].transform([room_class])[0]
            ],

            "booking_platform": [
                encoders["booking_platform"].transform([booking_platform])[0]
            ],

            "no_guests": [no_guests],

            # Month is already numeric
            "month": [month],

            "ratings_given": [rating]

        })

        prediction = model.predict(input_data)[0]

        booking_status = encoders["booking_status"].inverse_transform(
            [prediction]
        )[0]

        st.success(f"### Predicted Booking Status: {booking_status}")

    except Exception as e:

        st.error("Prediction Failed")
        st.exception(e)

# ----------------------------------------------------------
# Model Information
# ----------------------------------------------------------

st.markdown("---")

st.subheader("Model Information")

st.write("""
**Algorithm:** Random Forest Classifier

**Input Features**
- City
- Room Class
- Booking Platform
- Number of Guests
- Month
- Rating

**Target**
- Booking Status
""")

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

st.markdown("---")
st.caption("Hospitality Analytics Dashboard | ReadyNest Internship")