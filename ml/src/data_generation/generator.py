"""
Synthetic Logistics Shipment Data Generator
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
    VEHICLE_TYPES,
    WEATHER_CONDITIONS,
    TRAFFIC_LEVELS,
    ROUTE_TYPES,
)

from utils import haversine_distance

from business_rules import (
    get_vehicle_speed,
    calculate_expected_travel_hours,
    calculate_delivery_cost,
    calculate_delay,
)

# ==========================================================
# Initialize Faker & Random Seed
# ==========================================================

fake = Faker()

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

# ==========================================================
# Shipment ID Generator
# ==========================================================


def generate_shipment_id(index: int) -> str:
    """
    Generate a unique shipment ID.
    """
    return f"SHP{index:07d}"


# ==========================================================
# Datetime Generator
# ==========================================================


def generate_datetimes(
    distance_km: float,
    weather: str,
    traffic_level: str,
    vehicle_type: str,
    driver_experience: int,
    warehouse_load: str,
    customer_priority: str,
    is_holiday: bool,
):
    """
    Generate booking, dispatch,
    expected delivery and actual delivery timestamps.
    """

    # --------------------------------------------------
    # Booking Time
    # --------------------------------------------------

    booking = fake.date_time_between(
        start_date="-365d",
        end_date="now",
    )

    is_weekend = booking.weekday() >= 5

    # --------------------------------------------------
    # Dispatch Time
    # --------------------------------------------------

    dispatch = booking + timedelta(
        hours=random.randint(1, 24)
    )

    # --------------------------------------------------
    # Expected Travel Time
    # --------------------------------------------------

    expected_travel_hours = calculate_expected_travel_hours(
        distance_km,
        vehicle_type,
    )

    expected_delivery = dispatch + timedelta(
        hours=expected_travel_hours
    )

    # --------------------------------------------------
    # Calculate Delay
    # --------------------------------------------------

    delay_minutes = calculate_delay(
        weather=weather,
        traffic_level=traffic_level,
        distance_km=distance_km,
        vehicle_type=vehicle_type,
        driver_experience=driver_experience,
        warehouse_load=warehouse_load,
        customer_priority=customer_priority,
        is_weekend=is_weekend,
        is_holiday=is_holiday,
    )

    # --------------------------------------------------
    # Actual Delivery Time
    # --------------------------------------------------

    actual_delivery = expected_delivery + timedelta(
        minutes=delay_minutes
    )

    # Shipment delayed?
    delayed = delay_minutes > 60

    return (
        booking,
        dispatch,
        expected_delivery,
        actual_delivery,
        delay_minutes,
        delayed,
    )

# ==========================================================
# Record Generator
# ==========================================================

def generate_record(index: int):
    """
    Generate one realistic shipment record.
    """

    # --------------------------------------------------
    # Origin & Destination
    # --------------------------------------------------

    origin = random.choice(CITIES)

    destination = random.choice(
        [city for city in CITIES if city != origin]
    )

    # --------------------------------------------------
    # Coordinates & Distance
    # --------------------------------------------------

    origin_lat, origin_lon = CITY_COORDINATES[origin]

    destination_lat, destination_lon = CITY_COORDINATES[destination]

    distance = round(
        haversine_distance(
            origin_lat,
            origin_lon,
            destination_lat,
            destination_lon,
        ),
        2,
    )

    # --------------------------------------------------
    # Shipment Information
    # --------------------------------------------------

    package_type = random.choice(PACKAGE_TYPES)

    vehicle_type = random.choice(VEHICLE_TYPES)

    weather = random.choice(WEATHER_CONDITIONS)

    traffic_level = random.choice(TRAFFIC_LEVELS)

    route_type = random.choice(ROUTE_TYPES)

    shipment_weight = round(
        random.uniform(0.2, 40),
        2,
    )

    # --------------------------------------------------
    # Business Features
    # --------------------------------------------------

    driver_experience = random.randint(1, 15)

    warehouse_load = random.choice(
        [
            "Low",
            "Medium",
            "High",
        ]
    )

    customer_priority = random.choice(
        [
            "Standard",
            "Express",
            "Same Day",
        ]
    )

    fuel_price = round(
        random.uniform(90, 115),
        2,
    )

    fuel_consumption = round(
        distance / random.uniform(8, 15),
        2,
    )

    is_holiday = random.random() < 0.08

    # --------------------------------------------------
    # Business Rules
    # --------------------------------------------------

    vehicle_speed = get_vehicle_speed(
        vehicle_type
    )

    expected_travel_hours = (
        calculate_expected_travel_hours(
            distance,
            vehicle_type,
        )
    )

    delivery_cost = calculate_delivery_cost(
        distance,
        shipment_weight,
    )

    # --------------------------------------------------
    # Generate Times
    # --------------------------------------------------

    (
        booking,
        dispatch,
        expected_delivery,
        actual_delivery,
        delay_minutes,
        delayed,
    ) = generate_datetimes(
        distance_km=distance,
        weather=weather,
        traffic_level=traffic_level,
        vehicle_type=vehicle_type,
        driver_experience=driver_experience,
        warehouse_load=warehouse_load,
        customer_priority=customer_priority,
        is_holiday=is_holiday,
    )

    # --------------------------------------------------
    # Calendar Features
    # --------------------------------------------------

    is_weekend = booking.weekday() >= 5

    # --------------------------------------------------
    # Final Record
    # --------------------------------------------------

    return {

        "shipment_id": generate_shipment_id(index),

        "booking_datetime": booking,
        "dispatch_datetime": dispatch,
        "expected_delivery_datetime": expected_delivery,
        "actual_delivery_datetime": actual_delivery,

        "origin_city": origin,
        "destination_city": destination,

        "distance_km": distance,

        "package_type": package_type,

        "vehicle_type": vehicle_type,

        "vehicle_speed_kmph": vehicle_speed,

        "shipment_weight_kg": shipment_weight,

        "weather": weather,

        "traffic_level": traffic_level,

        "route_type": route_type,

        "driver_experience_years": driver_experience,

        "warehouse_load": warehouse_load,

        "customer_priority": customer_priority,

        "fuel_price_per_litre": fuel_price,

        "fuel_consumption_litres": fuel_consumption,

        "expected_travel_hours": expected_travel_hours,

        "delivery_cost": delivery_cost,

        "is_weekend": is_weekend,

        "is_holiday": is_holiday,

        "delay_minutes": delay_minutes,

        "delayed": delayed,
    }

# ==========================================================
# Dataset Generator
# ==========================================================

def generate_dataset():
    """
    Generate the complete logistics dataset.
    """

    data = [
        generate_record(i + 1)
        for i in range(NUM_RECORDS)
    ]

    return pd.DataFrame(data)


# ==========================================================
# Dataset Summary
# ==========================================================

def print_summary(df):
    """
    Print useful dataset statistics.
    """

    print("\n" + "=" * 70)
    print("LOGISTICS DATASET SUMMARY")
    print("=" * 70)

    print(f"\nTotal Shipments      : {len(df):,}")
    print(f"Delayed Shipments    : {df['delayed'].sum():,}")
    print(f"On-Time Shipments    : {(~df['delayed']).sum():,}")

    print(
        f"\nDelay Percentage     : "
        f"{df['delayed'].mean()*100:.2f}%"
    )

    print(
        f"Average Distance     : "
        f"{df['distance_km'].mean():.2f} km"
    )

    print(
        f"Average Delivery Cost: "
        f"₹{df['delivery_cost'].mean():.2f}"
    )

    print(
        f"Average Delay        : "
        f"{df['delay_minutes'].mean():.2f} minutes"
    )

    print(
        f"Maximum Delay        : "
        f"{df['delay_minutes'].max()} minutes"
    )

    print(
        f"Minimum Delay        : "
        f"{df['delay_minutes'].min()} minutes"
    )

    print("\nWeather Distribution")
    print(df["weather"].value_counts())

    print("\nTraffic Distribution")
    print(df["traffic_level"].value_counts())

    print("\nVehicle Distribution")
    print(df["vehicle_type"].value_counts())

    print("\nWarehouse Load Distribution")
    print(df["warehouse_load"].value_counts())

    print("\nCustomer Priority Distribution")
    print(df["customer_priority"].value_counts())

    print("\nDelay by Weather")
    print(
        df.groupby("weather")["delay_minutes"]
        .mean()
        .round(2)
    )

    print("\nDelay by Traffic")
    print(
        df.groupby("traffic_level")["delay_minutes"]
        .mean()
        .round(2)
    )

    print("\nDelay by Vehicle")
    print(
        df.groupby("vehicle_type")["delay_minutes"]
        .mean()
        .round(2)
    )

    print("\nDelay by Warehouse Load")
    print(
        df.groupby("warehouse_load")["delay_minutes"]
        .mean()
        .round(2)
    )

    print("\nDelay by Customer Priority")
    print(
        df.groupby("customer_priority")["delay_minutes"]
        .mean()
        .round(2)
    )

    print("=" * 70)


# ==========================================================
# Dataset Validation
# ==========================================================

def validate_dataset(df):
    """
    Validate generated dataset.
    """

    print("\n" + "=" * 70)
    print("DATA VALIDATION")
    print("=" * 70)

    print(
        f"Missing Values          : "
        f"{df.isnull().sum().sum()}"
    )

    print(
        f"Duplicate Shipment IDs  : "
        f"{df['shipment_id'].duplicated().sum()}"
    )

    print(
        f"Invalid Distance Rows   : "
        f"{(df['distance_km'] <= 0).sum()}"
    )

    print(
        f"Negative Delivery Cost  : "
        f"{(df['delivery_cost'] <= 0).sum()}"
    )

    print(
        f"Negative Delay Rows     : "
        f"{(df['delay_minutes'] < 0).sum()}"
    )

    print(
        f"Invalid Vehicle Speed   : "
        f"{(df['vehicle_speed_kmph'] <= 0).sum()}"
    )

    print(
        f"Duplicate Records       : "
        f"{df.duplicated().sum()}"
    )

    print("=" * 70)

    if (
        df.isnull().sum().sum() == 0
        and df["shipment_id"].duplicated().sum() == 0
        and (df["distance_km"] <= 0).sum() == 0
        and (df["delivery_cost"] <= 0).sum() == 0
        and (df["delay_minutes"] < 0).sum() == 0
    ):
        print("Dataset Validation PASSED")
    else:
        print("Dataset Validation FAILED")


# ==========================================================
# Save Processed Dataset
# ==========================================================

def save_processed_dataset(df):
    """
    Save processed dataset.
    """

    output_path = (
        "ml/data/processed/"
        "logistics_shipments_processed.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nProcessed dataset saved to:\n{output_path}"
    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("GENERATING SYNTHETIC LOGISTICS DATASET")
    print("=" * 70)

    # ------------------------------------------------------
    # Generate Dataset
    # ------------------------------------------------------

    df = generate_dataset()

    # ------------------------------------------------------
    # Save Raw Dataset
    # ------------------------------------------------------

    raw_path = (
        "ml/data/raw/"
        "logistics_shipments.csv"
    )

    df.to_csv(
        raw_path,
        index=False,
    )

    # ------------------------------------------------------
    # Save Processed Dataset
    # ------------------------------------------------------

    save_processed_dataset(df)

    # ------------------------------------------------------
    # Display Dataset
    # ------------------------------------------------------

    pd.set_option(
        "display.max_columns",
        None,
    )

    pd.set_option(
        "display.width",
        None,
    )

    print("\nColumns\n")
    print(df.columns.tolist())

    print("\nFirst Five Rows\n")
    print(df.head().to_string())

    # ------------------------------------------------------
    # Dataset Summary
    # ------------------------------------------------------

    print_summary(df)

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    validate_dataset(df)

    # ------------------------------------------------------
    # Delay Statistics
    # ------------------------------------------------------

    print("\nDelay Statistics")
    print(df["delay_minutes"].describe())

    print("\nDelayed Shipment Distribution")
    print(df["delayed"].value_counts())

    print("\nDelayed Shipment Percentage")
    print(df["delayed"].value_counts(normalize=True))

    # ------------------------------------------------------
    # Top Delay Reasons
    # ------------------------------------------------------

    print("\nAverage Delay by Weather")
    print(
        df.groupby("weather")["delay_minutes"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    print("\nAverage Delay by Traffic")
    print(
        df.groupby("traffic_level")["delay_minutes"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    print("\nAverage Delay by Warehouse Load")
    print(
        df.groupby("warehouse_load")["delay_minutes"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    print("\nAverage Delay by Customer Priority")
    print(
        df.groupby("customer_priority")["delay_minutes"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    # ------------------------------------------------------
    # Final Summary
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATA GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"\nTotal Records : {len(df):,}")
    print(f"Total Columns : {len(df.columns)}")

    print("\nDataset Shape")
    print(df.shape)

    print(f"\nRaw Dataset Saved To:\n{raw_path}")

    print(
        "\nProcessed Dataset Saved To:\n"
        "ml/data/processed/logistics_shipments_processed.csv"
    )

    print("\nReady for Model Training (Sprint 3)")