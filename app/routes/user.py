from uuid import UUID
from fastapi import APIRouter

from app.dependencies import current_user
from app.schemas.user import UserOut

router = APIRouter()



@router.get("/me")
async def get_current_user_details(user: current_user) -> UserOut:
    return UserOut.model_validate(user)
