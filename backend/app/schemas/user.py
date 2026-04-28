from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime
from app.domain.entities.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=1)
    role: UserRole

# Properties to return to client
class UserResponse(UserBase):
    id: uuid.UUID
    role: UserRole
    created_at: datetime
    
    model_config = {"from_attributes": True}
