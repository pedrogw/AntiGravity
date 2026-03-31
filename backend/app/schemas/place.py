from pydantic import BaseModel
import uuid

class FactoryBase(BaseModel):
    name: str
    lat: float
    lng: float

class FactoryCreate(FactoryBase):
    pass

class FactoryResponse(FactoryBase):
    id: uuid.UUID
    model_config = {"from_attributes": True}

class StoreBase(BaseModel):
    name: str
    lat: float
    lng: float
    owner_id: uuid.UUID

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: uuid.UUID
    model_config = {"from_attributes": True}
