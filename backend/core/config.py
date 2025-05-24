from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    #Main
    model_config = SettingsConfigDict (
        env_file=".env",
        case_sensitive=False,
    )
    #Base
    host: str = "0.0.0.0"
    port: int = 8000
    #DB
    db_url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    #Auth
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    lifetime_seconds: int = 2_592_000
    reset_password_token_secret: str
    verification_token_secret: str
    #Admin
    admin_password: str
    admin_email: str
    #Minio
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "products-images"
    minio_secure: bool = False
    minio_public_url: str = "localhost:9001"
    #Tests
    admin_token: str
    auth_user_token: str

settings = Settings()