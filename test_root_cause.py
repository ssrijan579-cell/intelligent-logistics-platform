from ml.src.explainability.root_cause import identify_root_causes

shipment = {
    "weather": "Storm",
    "traffic_level": "High",
    "warehouse_load": "High",
    "driver_experience_years": 2,
    "distance_km": 1500,
    "is_weekend": True,
    "is_holiday": False,
}

print(identify_root_causes(shipment))