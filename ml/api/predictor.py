"""
Model loading and prediction utilities.
"""

import joblib
import pandas as pd
from pathlib import Path

from ml.src.explainability.root_cause import identify_root_causes
from ml.src.explainability.recommendations import generate_recommendations

# ==========================================================
# Model Paths
# ==========================================================

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

classification_model = joblib.load(
    MODEL_DIR / "random_forest_model.pkl"
)

regression_model = joblib.load(
    MODEL_DIR / "delay_regression_model.pkl"
)

print("Classification model loaded.")
print("Regression model loaded.")

# ==========================================================
# Prediction Function
# ==========================================================

def predict_delay(request):
    """
    Predict shipment delay,
    estimated delay time,
    root causes,
    and recommendations.
    """

    # ======================================================
    # Classification Features
    # ======================================================

    classification_data = pd.DataFrame([{

        "origin_city": request.origin_city,
        "destination_city": request.destination_city,
        "distance_km": request.distance_km,
        "package_type": request.package_type,
        "vehicle_type": request.vehicle_type,
        "vehicle_speed_kmph": request.vehicle_speed_kmph,
        "shipment_weight_kg": request.shipment_weight_kg,
        "weather": request.weather,
        "traffic_level": request.traffic_level,
        "route_type": request.route_type,
        "driver_experience_years": request.driver_experience_years,
        "warehouse_load": request.warehouse_load,
        "customer_priority": request.customer_priority,
        "fuel_price_per_litre": request.fuel_price_per_litre,
        "fuel_consumption_litres": request.fuel_consumption_litres,
        "expected_travel_hours": request.expected_travel_hours,
        "delivery_cost": request.delivery_cost,
        "is_weekend": request.is_weekend,
        "is_holiday": request.is_holiday,
        "booking_month": request.booking_month,
        "booking_day": request.booking_day,
        "booking_weekday": request.booking_weekday,
        "booking_hour": request.booking_hour,

    }])

    # ======================================================
    # Regression Features
    # ======================================================

    regression_data = pd.DataFrame([{

        "origin_city": request.origin_city,
        "destination_city": request.destination_city,
        "distance_km": request.distance_km,
        "package_type": request.package_type,
        "vehicle_type": request.vehicle_type,
        "vehicle_speed_kmph": request.vehicle_speed_kmph,
        "shipment_weight_kg": request.shipment_weight_kg,
        "weather": request.weather,
        "traffic_level": request.traffic_level,
        "route_type": request.route_type,
        "driver_experience_years": request.driver_experience_years,
        "warehouse_load": request.warehouse_load,
        "customer_priority": request.customer_priority,
        "fuel_price_per_litre": request.fuel_price_per_litre,
        "fuel_consumption_litres": request.fuel_consumption_litres,
        "expected_travel_hours": request.expected_travel_hours,
        "delivery_cost": request.delivery_cost,
        "is_weekend": request.is_weekend,
        "is_holiday": request.is_holiday,

    }])

    # ======================================================
    # Predictions
    # ======================================================

    prediction = classification_model.predict(
        classification_data
    )[0]

    probability = classification_model.predict_proba(
        classification_data
    )[0][1]

    estimated_delay = regression_model.predict(
        regression_data
    )[0]

    estimated_delay = max(
        0,
        round(float(estimated_delay), 1),
    )

    # ======================================================
    # Shipment Dictionary
    # ======================================================

    shipment = regression_data.iloc[0].to_dict()

    causes = identify_root_causes(
        shipment
    )

    recommendations = generate_recommendations(
        shipment
    )

    # ======================================================
    # Response
    # ======================================================

    return {

        "prediction": (
            "Delayed"
            if prediction
            else "On Time"
        ),

        "probability": round(
            float(probability),
            4,
        ),

        "estimated_delay_minutes": estimated_delay,

        "root_causes": causes,

        "recommendations": recommendations,

    }