import streamlit as st
from api import predict_shipment

from datetime import datetime

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Intelligent Logistics Platform",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("🚚 Intelligent Logistics Platform")

st.sidebar.markdown("---")

st.sidebar.success("System Status")

st.sidebar.write("🟢 FastAPI Backend")

st.sidebar.write("🟢 Classification Model")

st.sidebar.write("🟢 Regression Model")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Models**

    • Random Forest Classifier

    • CatBoost Regressor

    • Root Cause Engine

    • Recommendation Engine
    """
)

# =====================================================
# Header
# =====================================================

st.title("🚚 Intelligent Logistics Platform")

st.caption(
    "AI-powered Shipment Delay Prediction System"
)

st.markdown("---")

# =====================================================
# Overview Metrics
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Classification Model",
        "Random Forest",
    )

with col2:
    st.metric(
        "Regression Model",
        "CatBoost",
    )

with col3:
    st.metric(
        "API",
        "Online",
    )

with col4:
    st.metric(
        "Version",
        "1.0",
    )

st.markdown("---")

# =====================================================
# Welcome
# =====================================================

st.subheader("Welcome")

st.write(
    """
This dashboard predicts whether a shipment will be delayed,
estimates the expected delay duration,
identifies possible root causes,
and provides operational recommendations.

Use the navigation menu on the left to explore the project.
"""
)

st.markdown("---")

st.subheader("Features")

# =====================================================
# Shipment Prediction Form
# =====================================================

st.header("📦 Shipment Details")

col1, col2 = st.columns(2)

# ---------------- Left Column ----------------

with col1:

    origin_city = st.selectbox(
        "Origin City",
        [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Chennai",
            "Hyderabad",
            "Kolkata",
            "Pune",
            "Ahmedabad",
        ],
    )

    package_type = st.selectbox(
        "Package Type",
        [
            "Electronics",
            "Clothing",
            "Food",
            "Furniture",
            "Medicine",
        ],
    )

    weather = st.selectbox(
        "Weather",
        [
            "Clear",
            "Rain",
            "Fog",
            "Storm",
        ],
    )

    route_type = st.selectbox(
        "Route Type",
        [
            "Highway",
            "City",
            "Rural",
        ],
    )

    shipment_weight = st.number_input(
        "Shipment Weight (kg)",
        min_value=0.5,
        max_value=500.0,
        value=20.0,
    )

    distance = st.number_input(
        "Distance (km)",
        min_value=10,
        max_value=3000,
        value=500,
    )

# ---------------- Right Column ----------------

with col2:

    destination_city = st.selectbox(
        "Destination City",
        [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Chennai",
            "Hyderabad",
            "Kolkata",
            "Pune",
            "Ahmedabad",
        ],
        index=1,
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "Truck",
            "Mini Truck",
            "Van",
        ],
    )

    traffic = st.selectbox(
        "Traffic Level",
        [
            "Low",
            "Medium",
            "High",
        ],
    )

    warehouse_load = st.selectbox(
        "Warehouse Load",
        [
            "Low",
            "Medium",
            "High",
        ],
    )

    customer_priority = st.selectbox(
        "Customer Priority",
        [
            "Standard",
            "Express",
            "Same Day",
        ],
    )

    driver_experience = st.slider(
        "Driver Experience (Years)",
        1,
        20,
        5,
    )

st.markdown("---")

predict_button = st.button(
    "🚀 Predict Shipment",
    use_container_width=True,
)

if predict_button:

    now = datetime.now()

    request = {

        "origin_city": origin_city,

        "destination_city": destination_city,

        "distance_km": float(distance),

        "package_type": package_type,

        "vehicle_type": vehicle_type,

        "vehicle_speed_kmph": 55,

        "shipment_weight_kg": float(shipment_weight),

        "weather": weather,

        "traffic_level": traffic,

        "route_type": route_type,

        "driver_experience_years": driver_experience,

        "warehouse_load": warehouse_load,

        "customer_priority": customer_priority,

        "fuel_price_per_litre": 102,

        "fuel_consumption_litres": 60,

        "expected_travel_hours": distance / 55,

        "delivery_cost": distance * 5,

        "is_weekend": now.weekday() >= 5,

        "is_holiday": False,

        "booking_month": now.month,

        "booking_day": now.day,

        "booking_weekday": now.weekday(),

        "booking_hour": now.hour,

    }

    with st.spinner("Running ML Models..."):

        result = predict_shipment(request)

    if "error" in result:

        st.error(result["error"])

    else:

        st.success("✅ Prediction Completed Successfully")

        st.markdown("---")

        # =====================================================
        # Prediction Summary
        # =====================================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction",
                result["prediction"],
            )

        with col2:
            st.metric(
                "Confidence",
                f"{result['probability']*100:.1f}%",
            )

        with col3:
            st.metric(
                "Estimated Delay",
                f"{result['estimated_delay_minutes']:.1f} min",
            )

        st.markdown("---")

        # =====================================================
        # Root Causes
        # =====================================================

        st.subheader("⚠️ Root Causes")

        for cause in result["root_causes"]:
            st.warning(cause)

        st.markdown("---")

        # =====================================================
        # Recommendations
        # =====================================================

        st.subheader("✅ Recommendations")

        for recommendation in result["recommendations"]:
            st.success(recommendation)