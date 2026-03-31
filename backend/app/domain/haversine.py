import math
from datetime import datetime, timedelta

def calculate_haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("Latitude out of bounds")
    if not (-180 <= lng1 <= 180 and -180 <= lng2 <= 180):
        raise ValueError("Longitude out of bounds")
        
    R = 6371.0 # Radius of earth in km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def calculate_eta(distance_km: float, speed_kmh: float) -> float:
    if speed_kmh <= 0:
        raise ValueError("Speed must be positive")
    if distance_km < 0:
        raise ValueError("Distance cannot be negative")
    if distance_km == 0:
        return 0.0
        
    return distance_km / speed_kmh

def add_hours_to_now(hours: float) -> datetime:
    return datetime.utcnow() + timedelta(hours=hours)
