import uuid
import datetime
import enum
from dataclasses import dataclass, field

class UserRole(str, enum.Enum):
    lojista = "lojista"
    motorista = "motorista"

@dataclass
class User:
    email: str
    password_hash: str
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
