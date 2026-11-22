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
# ==========================================================
# Customer Experience & Feedback Intelligence
# ==========================================================

import csv
import os
import secrets
import sqlite3

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, Header, HTTPException, Query, status

from .schemas import FeedbackCreate

from .feedback_db import (
    create_feedback,
    get_all_feedback,
    get_feedback_summary,
)


# ==========================================================
# Shipment ID Validation
# ==========================================================

SHIPMENT_DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "logistics_shipments_processed.csv"
)


@lru_cache(maxsize=1)
def get_valid_shipment_ids():

    if not SHIPMENT_DATA_PATH.exists():
        raise RuntimeError("Shipment dataset is unavailable.")

    with open(
        SHIPMENT_DATA_PATH,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        return frozenset(
            row["shipment_id"].strip()
            for row in reader
            if row.get("shipment_id")
        )


# ==========================================================
# Admin Authentication
# ==========================================================

def verify_admin_key(
    admin_key: str = Header(
        default=None,
        alias="X-Admin-API-Key",
    ),
):

    configured_key = os.getenv("FEEDBACK_ADMIN_API_KEY")

    if not configured_key:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin authentication is not configured.",
        )

    if (
        not admin_key
        or not secrets.compare_digest(
            admin_key,
            configured_key,
        )
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrator credentials.",
        )


# ==========================================================
# Customer Feedback Submission
# ==========================================================

@app.post(
    "/feedback",
    status_code=status.HTTP_201_CREATED,
)
def submit_feedback(feedback: FeedbackCreate):

    try:

        valid_ids = get_valid_shipment_ids()

    except RuntimeError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Shipment validation service is unavailable.",
        )

    if feedback.shipment_id not in valid_ids:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment ID was not found.",
        )

    feedback_data = feedback.model_dump()

    feedback_data["shipment_id"] = (
        feedback_data["shipment_id"].strip().upper()
    )

    feedback_data["comments"] = (
        feedback_data["comments"].strip()
    )

    if len(feedback_data["comments"]) < 5:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Feedback comments must contain at least 5 characters.",
        )

    try:

        result = create_feedback(feedback_data)

        return {
            "message": "Feedback submitted successfully.",
            "feedback_id": result["feedback_id"],
            "shipment_id": result["shipment_id"],
            "created_at": result["created_at"],
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feedback has already been submitted for this shipment.",
        )


# ==========================================================
# Administrator: Retrieve Feedback
# ==========================================================

@app.get(
    "/feedback/admin",
    dependencies=[
        Depends(verify_admin_key)
    ],
)
def admin_get_feedback(

    limit: int = Query(default=100, ge=1, le=500),

    offset: int = Query(default=0, ge=0),

):

    return {
        "feedback": get_all_feedback(
            limit=limit,
            offset=offset,
        ),
        "limit": limit,
        "offset": offset,
    }


# ==========================================================
# Administrator: Feedback Analytics
# ==========================================================

@app.get(
    "/feedback/admin/summary",
    dependencies=[
        Depends(verify_admin_key)
    ],
)
def admin_feedback_summary():

    return get_feedback_summary()

