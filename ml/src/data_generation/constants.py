"""
Constants for synthetic logistics data generation.
"""

# Major Indian cities with latitude and longitude
CITY_COORDINATES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577),
    "Patna": (25.5941, 85.1376),
    "Bhopal": (23.2599, 77.4126),
    "Surat": (21.1702, 72.8311),
    "Chandigarh": (30.7333, 76.7794),
    "Guwahati": (26.1445, 91.7362),
    "Bhubaneswar": (20.2961, 85.8245),
    "Dehradun": (30.3165, 78.0322),
}

# List of cities
CITIES = list(CITY_COORDINATES.keys())

# Package categories
PACKAGE_TYPES = [
    "Document",
    "Parcel",
    "Fragile",
    "Electronics",
    "Medicine",
    "Furniture",
]

# Vehicle categories
VEHICLE_TYPES = [
    "Bike",
    "Van",
    "Mini Truck",
    "Truck",
]

# Weather conditions
WEATHER_CONDITIONS = [
    "Clear",
    "Rain",
    "Fog",
    "Storm",
]

# Route types
ROUTE_TYPES = [
    "Local",
    "Highway",
    "Mixed",
]

TRAFFIC_LEVELS = [
    "Low",
    "Medium",
    "High",
]
TRAFFIC_LEVELS = [
    "Low",
    "Medium",
    "High",
]