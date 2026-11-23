from http.client import HTTPException

import base62
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_config import counter
from app.models.urls import URL
from app.schemas.urls import URLIn, URLOut


async def get_short_url(
    session: AsyncSession, 
    url: URLIn,
    user_id: str
) -> URLOut:
    count = int(await counter())
    encoded_code = base62.encode(n=count)

    current_url = URL(**url.model_dump(), short_code=encoded_code, user_id=user_id)

    session.add(current_url)
    await session.commit()
    await session.refresh(current_url)

    return URLOut.model_validate(current_url)


async def open_short_url(
    session: AsyncSession,
    short_code: str
) -> URLOut:

    url = await session.get(URL, short_code)

    if not url:
        raise HTTPException(404, "url not found")
    
    return URLOut.model_validate(url)
