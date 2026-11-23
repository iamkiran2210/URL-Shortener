from pydantic import BaseModel


class Token(BaseModel):
    message: str
    access_token: str
    refresh_token: str
