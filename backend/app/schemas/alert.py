from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class AlertResponse(BaseModel):
    id: uuid.UUID
    delivery_id: uuid.UUID
    message: str
    is_critical: bool
    created_at: datetime
    dismissed_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
