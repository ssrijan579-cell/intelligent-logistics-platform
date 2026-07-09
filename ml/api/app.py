"""
FastAPI application for Intelligent Logistics Platform.
"""

from fastapi import FastAPI

from .schemas import (
    ShipmentRequest,
    PredictionResponse,
)

from .predictor import predict_delay


# =====================================================
# Create FastAPI App
# =====================================================

app = FastAPI(
    title="Intelligent Logistics Platform API",
    description="Machine Learning API for Shipment Delay Prediction",
    version="1.0.0",
)

# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Intelligent Logistics Platform",
        "version": "1.0.0",
        "status": "Running",
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "model": "Random Forest",
    }


# =====================================================
# Model Information
# =====================================================

@app.get("/model-info")
def model_info():

    return {

        "classification_model": "Random Forest",

        "regression_model": "CatBoost",

        "problem_types": [

            "Binary Classification",

            "Regression",

        ],

        "outputs": [

            "Delay Prediction",

            "Delay Minutes",

            "Root Causes",

            "Recommendations",

        ],

    }

# =====================================================
# Prediction Endpoint
# =====================================================

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: ShipmentRequest,
):
    """
    Predict shipment delay.
    """
    result = predict_delay(request)

    return PredictionResponse(

    prediction=result["prediction"],

    probability=result["probability"],

    estimated_delay_minutes=result[
        "estimated_delay_minutes"
    ],

    root_causes=result[
        "root_causes"
    ],

    recommendations=result[
        "recommendations"
    ],

)