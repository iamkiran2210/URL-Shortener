from fastapi import APIRouter

from app.schemas.user import UserIn, UserOut
from app.schemas.token import Token
from app.dependencies import db_session
from app.services.user_services import create_a_user, login_user


router = APIRouter()

@router.post("/register")
async def register_user(
    user: UserIn,
    db: db_session,
) -> UserOut:
    return UserOut.model_validate(
        await create_a_user(db, user)
    )

@router.post("/login")
async def login(
    user: UserIn,
    db: db_session,
) -> Token:
    return Token.model_validate(
        await login_user(db, user)
    )
