from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class URLIn(BaseModel):
    long_url: str


class URLOut(URLIn):
    model_config = ConfigDict(from_attributes=True)
    short_code: str
    created_at: datetime
