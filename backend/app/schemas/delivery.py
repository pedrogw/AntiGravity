from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class DeliveryBase(BaseModel):
    factory_id: uuid.UUID
    store_id: uuid.UUID
    driver_id: uuid.UUID

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryResponse(DeliveryBase):
    id: uuid.UUID
    status: str
    eta_original: Optional[datetime]
    eta_current: Optional[datetime]
    departed_at: Optional[datetime]
    model_config = {"from_attributes": True}
