"""
Synthetic logistics shipment data generator.
"""

import random
from datetime import timedelta

import pandas as pd
from faker import Faker

from config import NUM_RECORDS, RANDOM_SEED
from constants import (
    CITY_COORDINATES,
    CITIES,
    PACKAGE_TYPES,
    ROUTE_TYPES,
    VEHICLE_TYPES,
    WEATHER_CONDITIONS,
)
from utils import haversine_distance


# ---------------------------------
# Initialize Faker and Random
# ---------------------------------

fake = Faker()

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)


# ---------------------------------
# Helper Functions
# ---------------------------------

def generate_shipment_id(index: int) -> str:
    """Generate a unique shipment ID."""
    return f"SHP{index:07d}"


def generate_datetimes(distance_km):
    """
    Generate booking, dispatch, expected delivery,
    actual delivery and delay information.
    """

    booking = fake.date_time_between(
        start_date="-365d",
        end_date="now",
    )

    dispatch = booking + timedelta(
        hours=random.randint(1, 24)
    )

    # Approximate travel speed
    travel_hours = distance_km / 45

    expected = dispatch + timedelta(
        hours=travel_hours
    )

    delay_minutes = max(
        0,
        int(random.gauss(30, 40))
    )

    actual = expected + timedelta(
        minutes=delay_minutes
    )

    delayed = delay_minutes > 30

    return (
        booking,
        dispatch,
        expected,
        actual,
        delay_minutes,
        delayed,
    )


# ---------------------------------
# Record Generator
# ---------------------------------

def generate_record(index: int) -> dict:
    """Generate one shipment record."""

    origin = random.choice(CITIES)

    destination = random.choice(
        [city for city in CITIES if city != origin]
    )

    origin_lat, origin_lon = CITY_COORDINATES[origin]
    destination_lat, destination_lon = CITY_COORDINATES[destination]

    distance = haversine_distance(
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon,
    )

    (
        booking,
        dispatch,
        expected,
        actual,
        delay_minutes,
        delayed,
    ) = generate_datetimes(distance)

    return {
        "shipment_id": generate_shipment_id(index),

        "origin_city": origin,
        "destination_city": destination,

        "distance_km": distance,

        "booking_datetime": booking,
        "dispatch_datetime": dispatch,
        "expected_delivery_datetime": expected,
        "actual_delivery_datetime": actual,

        "delay_minutes": delay_minutes,
        "delayed": delayed,

        "package_type": random.choice(PACKAGE_TYPES),
        "vehicle_type": random.choice(VEHICLE_TYPES),
        "weather": random.choice(WEATHER_CONDITIONS),
        "route_type": random.choice(ROUTE_TYPES),

        "shipment_weight_kg": round(
            random.uniform(0.2, 40),
            2,
        ),
    }


# ---------------------------------
# Dataset Generator
# ---------------------------------

def generate_dataset():
    """Generate the complete dataset."""

    data = [
        generate_record(i + 1)
        for i in range(NUM_RECORDS)
    ]

    return pd.DataFrame(data)


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    df = generate_dataset()

    output_path = "ml/data/raw/logistics_shipments.csv"

    df.to_csv(output_path, index=False)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print(f"\nGenerated {len(df)} shipment records.")
    print(f"Saved to: {output_path}")