import uuid
from dataclasses import dataclass, field
from app.domain.value_objects.coordinates import Coordinates

@dataclass
class Factory:
    name: str
    location: Coordinates
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Store:
    name: str
    location: Coordinates
    owner_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
