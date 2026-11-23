from http.client import HTTPException

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.core.security import decode_token


security = HTTPBearer()

credential = Annotated[HTTPAuthorizationCredentials, Depends(security)]

db_session = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    db: db_session,
    credentials: credential
) -> User:

    token = decode_token(credentials.credentials)

    if "sub" not in token or not token["sub"]:
        raise HTTPException(401, "Unauthorized") 
            
    user = await db.get(User, token['sub'])

    if not user:
        raise HTTPException(404, "user not found")


    return user

current_user = Annotated[User, Depends(get_current_user)]
    