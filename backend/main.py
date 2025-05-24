from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from api import router as api
from core.config import settings
from core.models import db_helper
from utils.minio import create_bucket
@asynccontextmanager
async def lifespan(app):
    await create_bucket()
    yield
    #shutdown
    await db_helper.dispose()

main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
main_app.include_router(api, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.host, port=settings.port)