"""
Recommendation Engine
Provides business recommendations to reduce shipment delays.
"""


def generate_recommendations(shipment):
    """
    Generate recommendations based on shipment details.

    Parameters
    ----------
    shipment : dict

    Returns
    -------
    list
    """

    recommendations = []

    # ==========================================
    # Weather
    # ==========================================

    weather = shipment.get("weather", "")

    if weather == "Storm":

        recommendations.append(
            "Delay dispatch until weather improves if possible."
        )

        recommendations.append(
            "Monitor live weather alerts during transit."
        )

    elif weather == "Rain":

        recommendations.append(
            "Allocate additional travel time for wet roads."
        )

    elif weather == "Fog":

        recommendations.append(
            "Use experienced drivers for low-visibility conditions."
        )

    # ==========================================
    # Traffic
    # ==========================================

    traffic = shipment.get("traffic_level", "")

    if traffic == "High":

        recommendations.append(
            "Use alternate routes to avoid congestion."
        )

        recommendations.append(
            "Dispatch outside peak traffic hours."
        )

    elif traffic == "Medium":

        recommendations.append(
            "Monitor live traffic updates."
        )

    # ==========================================
    # Warehouse
    # ==========================================

    warehouse = shipment.get("warehouse_load", "")

    if warehouse == "High":

        recommendations.append(
            "Increase warehouse staffing during peak hours."
        )

        recommendations.append(
            "Prioritize high-value shipments."
        )

    # ==========================================
    # Driver Experience
    # ==========================================

    experience = shipment.get(
        "driver_experience_years",
        0,
    )

    if experience < 3:

        recommendations.append(
            "Assign a more experienced driver."
        )

    # ==========================================
    # Distance
    # ==========================================

    distance = shipment.get("distance_km", 0)

    if distance > 1200:

        recommendations.append(
            "Consider splitting the route into multiple delivery hubs."
        )

        recommendations.append(
            "Schedule additional driver rest breaks."
        )

    # ==========================================
    # Weekend
    # ==========================================

    if shipment.get("is_weekend"):

        recommendations.append(
            "Plan dispatch earlier on weekends."
        )

    # ==========================================
    # Holiday
    # ==========================================

    if shipment.get("is_holiday"):

        recommendations.append(
            "Increase fleet capacity during holiday periods."
        )

    # ==========================================
    # Customer Priority
    # ==========================================

    priority = shipment.get(
        "customer_priority",
        "",
    )

    if priority == "Same Day":

        recommendations.append(
            "Assign the fastest available vehicle."
        )

    elif priority == "Express":

        recommendations.append(
            "Prioritize loading and dispatch."
        )

    # ==========================================
    # Default
    # ==========================================

    if not recommendations:

        recommendations.append(
            "Shipment appears low risk. Continue normal operations."
        )

    return recommendations