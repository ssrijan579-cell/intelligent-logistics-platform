"""
Pydantic schemas for the Logistics Prediction API.
"""

from typing import List

from pydantic import BaseModel


# =====================================================
# Request Schema
# =====================================================

class ShipmentRequest(BaseModel):

    origin_city: str
    destination_city: str

    distance_km: float

    package_type: str
    vehicle_type: str
    vehicle_speed_kmph: int

    shipment_weight_kg: float

    weather: str
    traffic_level: str
    route_type: str

    driver_experience_years: int
    warehouse_load: str
    customer_priority: str

    fuel_price_per_litre: float
    fuel_consumption_litres: float

    expected_travel_hours: float
    delivery_cost: float

    is_weekend: bool
    is_holiday: bool

    booking_month: int
    booking_day: int
    booking_weekday: int
    booking_hour: int


# =====================================================
# Response Schema
# =====================================================

class PredictionResponse(BaseModel):

    prediction: str

    probability: float

    estimated_delay_minutes: float

    root_causes: List[str]

    recommendations: List[str]

# ==========================================================
# Customer Feedback Schemas
# ==========================================================

from pydantic import Field


class FeedbackCreate(BaseModel):

    shipment_id: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^SHP\d{7}$",
    )

    overall_rating: int = Field(ge=1, le=5)

    delivery_rating: int = Field(ge=1, le=5)

    agent_rating: int = Field(ge=1, le=5)

    packaging_rating: int = Field(ge=1, le=5)

    comments: str = Field(
        min_length=5,
        max_length=2000,
    )
