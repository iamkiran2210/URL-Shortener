from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    created_at: datetime
