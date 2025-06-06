from fastapi import APIRouter
from .Dependencies.fastapi_users_object import fastapi_users
from core.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
from .Dependencies.backend import authentication_backend
#/login
#/logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend, requires_verification=True),
)

#register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

#/request-verify-token
#/verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

#/forgot-password
#/reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)