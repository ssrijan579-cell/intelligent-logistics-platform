"""
Business rules for Intelligent Logistics Platform.
"""

import random


# ==========================================================
# Vehicle Speed
# ==========================================================

def get_vehicle_speed(vehicle_type):
    """
    Average speed (km/h) by vehicle type.
    """

    speed = {
        "Bike": 45,
        "Van": 55,
        "Mini Truck": 50,
        "Truck": 40,
    }

    return speed.get(vehicle_type, 45)


# ==========================================================
# Expected Travel Time
# ==========================================================

def calculate_expected_travel_hours(
    distance_km,
    vehicle_type,
):
    """
    Calculate expected travel hours.
    """

    speed = get_vehicle_speed(vehicle_type)

    travel_time = distance_km / speed

    # Loading / unloading time
    travel_time += random.uniform(0.5, 2.0)

    return round(travel_time, 2)


# ==========================================================
# Delivery Cost
# ==========================================================

def calculate_delivery_cost(
    distance_km,
    shipment_weight,
):
    """
    Calculate realistic delivery cost.
    """

    base_charge = 120

    distance_charge = distance_km * 1.45

    weight_charge = shipment_weight * 15

    total = (
        base_charge
        + distance_charge
        + weight_charge
    )

    return round(total, 2)


# ==========================================================
# Delay Calculation
# ==========================================================

def calculate_delay(
    weather,
    traffic_level,
    distance_km,
    vehicle_type,
    driver_experience,
    warehouse_load,
    customer_priority,
    is_weekend,
    is_holiday,
):
    """
    Generate realistic delivery delay (minutes).
    """

    delay = 0

    # ------------------------------------------------------
    # Weather
    # ------------------------------------------------------

    weather_delay = {
        "Clear": random.randint(0, 5),
        "Fog": random.randint(10, 25),
        "Rain": random.randint(20, 45),
        "Storm": random.randint(45, 90),
    }

    delay += weather_delay.get(weather, 0)

    # ------------------------------------------------------
    # Traffic
    # ------------------------------------------------------

    traffic_delay = {
        "Low": random.randint(0, 5),
        "Medium": random.randint(10, 20),
        "High": random.randint(25, 45),
    }

    delay += traffic_delay.get(traffic_level, 0)

    # ------------------------------------------------------
    # Distance
    # ------------------------------------------------------

    if distance_km > 1800:
        delay += random.randint(25, 40)

    elif distance_km > 1200:
        delay += random.randint(15, 25)

    elif distance_km > 700:
        delay += random.randint(5, 15)

    # ------------------------------------------------------
    # Vehicle
    # ------------------------------------------------------

    vehicle_delay = {
        "Bike": random.randint(-5, 5),
        "Van": random.randint(0, 8),
        "Mini Truck": random.randint(5, 12),
        "Truck": random.randint(10, 20),
    }

    delay += vehicle_delay.get(vehicle_type, 0)

    # ------------------------------------------------------
    # Driver Experience
    # ------------------------------------------------------

    if driver_experience <= 2:
        delay += random.randint(15, 30)

    elif driver_experience <= 5:
        delay += random.randint(5, 15)

    elif driver_experience >= 10:
        delay -= random.randint(5, 15)

    # ------------------------------------------------------
    # Warehouse Load
    # ------------------------------------------------------

    warehouse_delay = {
        "Low": 0,
        "Medium": random.randint(5, 12),
        "High": random.randint(15, 30),
    }

    delay += warehouse_delay[warehouse_load]

    # ------------------------------------------------------
    # Customer Priority
    # ------------------------------------------------------

    priority_bonus = {
        "Standard": 0,
        "Express": -10,
        "Same Day": -20,
    }

    delay += priority_bonus[customer_priority]

    # ------------------------------------------------------
    # Weekend
    # ------------------------------------------------------

    if is_weekend:
        delay += random.randint(5, 12)

    # ------------------------------------------------------
    # Holiday
    # ------------------------------------------------------

    if is_holiday:
        delay += random.randint(15, 30)

    # ------------------------------------------------------
    # Feature Interactions
    # ------------------------------------------------------

    if weather == "Storm" and traffic_level == "High":
        delay += random.randint(20, 40)

    if weather == "Rain" and vehicle_type == "Bike":
        delay += random.randint(10, 20)

    if warehouse_load == "High" and customer_priority == "Same Day":
        delay -= random.randint(5, 15)

    # ------------------------------------------------------
    # Rare Operational Incidents
    # ------------------------------------------------------

    incident = random.random()

    if incident < 0.01:
        # Major accident
        delay += random.randint(80, 150)

    elif incident < 0.03:
        # Vehicle breakdown
        delay += random.randint(40, 80)

    elif incident < 0.08:
        # Route diversion
        delay += random.randint(15, 35)

    # ------------------------------------------------------
    # General randomness
    # ------------------------------------------------------

    delay += random.randint(-10, 10)

    return max(0, round(delay))