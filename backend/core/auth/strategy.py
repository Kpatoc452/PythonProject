from fastapi_users.authentication import JWTStrategy
from core.config import settings

PRIVATE_KEY = settings.private_key_path.read_text()

PUBLIC_KEY = settings.public_key_path.read_text()

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=PRIVATE_KEY, 
        lifetime_seconds=settings.lifetime_seconds,
        algorithm=settings.algorithm,
        public_key=PUBLIC_KEY,
    )