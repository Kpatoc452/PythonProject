from minio import Minio
from fastapi import UploadFile, HTTPException, status
from core.config import settings
from uuid import uuid4
import os
import io
minio_client = Minio(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure
)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


async def upload_image_to_minio(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Недопустимый тип файла"
        )
    
    if file.size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Файл для загрузки слишком большой"
        )
    
    file_data = await file.read()
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid4()}{file_ext}"
    try:
        minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=file_name,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка загрузки изображения: {str(e)}"
        )
    
    return f"{settings.minio_public_url}/{settings.minio_bucket}/{file_name}"

async def get_object(obj_name: str):
    try:
        response = minio_client.get_object(settings.minio_bucket, obj_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения изображения: {str(e)}"
        )
    return response

async def create_bucket():
    try:
        if not minio_client.bucket_exists(settings.minio_bucket):
            minio_client.make_bucket(settings.minio_bucket)
    except Exception as e:
        print(f"Ошибка при создании баккета: {e}")

async def remove_file_from_minio(file_name: str):
    try:
        minio_client.remove_object(
            bucket_name=settings.minio_bucket,
            object_name=file_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка удаления изображения: {str(e)}"
        )