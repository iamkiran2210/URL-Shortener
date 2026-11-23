from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from argon2 import PasswordHasher

from app.core.config import settings
from app.schemas.token import Token
from app.models.user import User

hasher = PasswordHasher()


def hash_password(password: str):
    """
    Generates a hash password
    """
    return hasher.hash(password=password)


def verify_password(password: str, hash: str):
    return hasher.verify(password=password, hash=hash)


def create_access_token(user_id: str, expiry_time_minutes: float | None = None) -> str:

    iat = datetime.now(UTC)
    exp = datetime.now(UTC) + (
        timedelta(minutes=expiry_time_minutes)
        if expiry_time_minutes
        else timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
    )

    payload = {"sub": user_id, "iat": iat, "exp": exp}

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: str, expiry_time_minutes: float | None = None) -> str:

    iat = datetime.now(UTC)
    exp = datetime.now(UTC) + (
        timedelta(minutes=expiry_time_minutes)
        if expiry_time_minutes
        else timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRES_MINUTES)
    )

    payload = {"sub": user_id, "iat": iat, "exp": exp}

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_token(user: User, message: str):
    user_id = str(user.id)

    return Token(
        message=message,
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


def decode_token(token: str) -> dict:

    try:
        return jwt.decode(
            token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        return {"error": "Token Expired"}

    except jwt.InvalidTokenError:
        return {"error": "Invalid Token"}
