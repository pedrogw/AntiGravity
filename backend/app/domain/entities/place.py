import uuid
from dataclasses import dataclass, field

@dataclass
class Factory:
    name: str
    lat: float
    lng: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Store:
    name: str
    lat: float
    lng: float
    owner_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
