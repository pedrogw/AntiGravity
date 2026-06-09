import uuid
from dataclasses import dataclass, field
from app.domain.value_objects.coordinates import Coordinates

@dataclass
class Factory:
    """Fábrica de origem das entregas, com coordenada geográfica."""
    name: str
    location: Coordinates
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Store:
    """Loja de destino das entregas, vinculada a um lojista (owner_id)."""
    name: str
    location: Coordinates
    owner_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
