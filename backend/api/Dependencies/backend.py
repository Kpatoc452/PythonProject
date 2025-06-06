from fastapi_users.authentication import AuthenticationBackend

from core.auth.transport import bearer_transport
from core.auth.strategy import get_jwt_strategy

authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)