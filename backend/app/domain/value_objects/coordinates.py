from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinates:
    """Par de coordenadas geográficas (latitude/longitude)."""
    lat: float
    lng: float
