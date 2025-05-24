from fastapi_users import FastAPIUsers

from core.models import User
from .user_manager import get_user_manager
from .backend import authentication_backend

fastapi_users = FastAPIUsers[User, int] (
    get_user_manager,
    [authentication_backend],
)

current_optional_user = fastapi_users.current_user(optional=True)
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)