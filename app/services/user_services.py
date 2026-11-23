from http.client import HTTPException
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserIn, UserOut
from app.schemas.token import Token
from app.core.security import create_token

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_a_user(session: AsyncSession, user: UserIn) -> UserOut:
    user_dict = UserIn.model_dump(user)
    user_dict["hashed_password"] = user_dict.pop("password")
    current_user = User(**user_dict)

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return UserOut.model_validate(current_user)


async def login_user(
    session: AsyncSession,
    user: UserIn
) -> Token:

    current_user = await get_a_user(session, user)

    if not current_user:
        raise HTTPException(401, "unauthorized")
        
    return create_token(message="login successful", user=current_user)



async def get_a_user(session: AsyncSession, user: UserIn) -> User:
    result = await session.execute(
        select(User).where(User.username == user.username)
    )

    current_user = result.scalar_one_or_none()

    if not current_user:
        raise HTTPException(404, "User not found")

    return current_user



