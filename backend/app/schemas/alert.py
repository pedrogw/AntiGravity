from pydantic import BaseModel
from datetime import datetime
import uuid

class AlertResponse(BaseModel):
    id: uuid.UUID
    delivery_id: uuid.UUID
    message: str
    is_critical: bool
    created_at: datetime
    model_config = {"from_attributes": True}
