from typing import AsyncGenerator

from click import echo
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.base import Base


async_engine = create_async_engine(
    url=settings.DB_URL.encoded_string(),
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def create_schema():
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session
