from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.dependencies import current_user, db_session
from app.schemas.urls import URLIn, URLOut
from app.services.url_services import get_short_url, open_short_url

router = APIRouter()


@router.post("/")
async def get_short_link(
    url: URLIn,
    user: current_user,
    db: db_session
) -> URLOut:
    return URLOut.model_validate(await get_short_url(db, url, str(user.id)))


@router.get("/")
async def get_url(
    short_code: str,
    db: db_session
):
    url = await open_short_url(db, short_code)

    print(url)

    return RedirectResponse(url=f"https://{url.long_url}", status_code=307)
    
