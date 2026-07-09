"""
Root Cause Analysis Module
Determines the likely causes of shipment delays.
"""


def identify_root_causes(shipment):
    """
    Identify likely causes of shipment delay.

    Parameters
    ----------
    shipment : dict

    Returns
    -------
    list
    """

    causes = []

    # ==========================================
    # Weather
    # ==========================================

    weather = shipment.get("weather", "")

    if weather == "Storm":

        causes.append(
            "Stormy weather slowed transportation."
        )

    elif weather == "Rain":

        causes.append(
            "Rain increased travel time."
        )

    elif weather == "Fog":

        causes.append(
            "Low visibility due to fog."
        )

    # ==========================================
    # Traffic
    # ==========================================

    traffic = shipment.get(
        "traffic_level",
        "",
    )

    if traffic == "High":

        causes.append(
            "Heavy traffic congestion."
        )

    elif traffic == "Medium":

        causes.append(
            "Moderate traffic delays."
        )

    # ==========================================
    # Warehouse
    # ==========================================

    warehouse = shipment.get(
        "warehouse_load",
        "",
    )

    if warehouse == "High":

        causes.append(
            "Warehouse operating at high capacity."
        )

    # ==========================================
    # Driver Experience
    # ==========================================

    experience = shipment.get(
        "driver_experience_years",
        0,
    )

    if experience < 3:

        causes.append(
            "Low driver experience."
        )

    # ==========================================
    # Distance
    # ==========================================

    distance = shipment.get(
        "distance_km",
        0,
    )

    if distance > 1200:

        causes.append(
            "Long-distance shipment."
        )

    # ==========================================
    # Weekend
    # ==========================================

    if shipment.get("is_weekend"):

        causes.append(
            "Weekend operational delays."
        )

    # ==========================================
    # Holiday
    # ==========================================

    if shipment.get("is_holiday"):

        causes.append(
            "Holiday logistics disruption."
        )

    # ==========================================
    # Default
    # ==========================================

    if len(causes) == 0:

        causes.append(
            "No major delay factors detected."
        )

    return causes