from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
import uuid

class UsersSchemaPOST(BaseModel):
    username: str
    email: EmailStr
    password: bytes
    model_config = ConfigDict(from_attributes=True)

class UsersSchemaGET(UsersSchemaPOST):
    id: uuid.UUID
    password: bytes = Field(..., exclude=True)
    active: bool
    created_at: datetime
    updated_ad: datetime

class UsersSchemaPUT(UsersSchemaPOST):
    id: uuid.UUID