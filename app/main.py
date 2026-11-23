
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_schema
from app.core.redis_config import r
from app.routes.auth import router as auth_router
from app.routes.urls import router as url_router
from app.routes.user import router as user_router


async def lifespan(application: FastAPI):
    await create_schema()

    yield

    await r.aclose()


app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=['auth'])
app.include_router(user_router, prefix="/user", tags=['user', 'auth'])
app.include_router(url_router, prefix="/urls", tags=['urls'])

