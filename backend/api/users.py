from fastapi import APIRouter

from api.Dependencies.fastapi_users_object import fastapi_users
from core.schemas.user import UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

#/me
#/{id}
router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
)