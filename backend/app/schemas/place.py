from pydantic import BaseModel, Field
import uuid

class FactoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class FactoryCreate(FactoryBase):
    pass

class FactoryResponse(FactoryBase):
    id: uuid.UUID
    model_config = {"from_attributes": True}

class StoreBase(BaseModel):
    name: str = Field(..., min_length=1)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    owner_id: uuid.UUID

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: uuid.UUID
    model_config = {"from_attributes": True}
