import asyncio
import contextlib 


from api.Dependencies.user_manager import get_user_manager
from api.Dependencies.users import get_user_db
from core.models import User
from core.config import settings
from core.schemas.user import UserCreate
from core.models import db_helper
from core.auth.user_manager import UserManager


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user

async def create_superuser():
    user_create = UserCreate(
        email=settings.admin_email,
        password=settings.admin_password,
        is_active=True,
        is_superuser=True,
        is_verified=True
    )
    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(
                    user_manager=user_manager, 
                    user_create=user_create,
                )

if __name__ == "__main__":
    asyncio.run(create_superuser)