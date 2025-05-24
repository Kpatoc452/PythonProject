from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from api.Dependencies.fastapi_users_object import current_active_user, current_optional_user
from core.schemas.product import ProductUpdate, ProductRead
from core.models.db_helper import db_helper
from core.models.user import User
from core.models.product import Product
from core.models.product_views import ProductViews
from crud.products import ProductCRUD
from crud.product_views import ViewsCRUD
from utils.minio import upload_image_to_minio, remove_file_from_minio, get_object

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post('')
async def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category_id: int = Form(...), 
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter), 
    user: User = Depends(current_active_user)
):
    image_url: str = await upload_image_to_minio(file)
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "category_id": category_id,
        "seller_id": user.id,
        "image": image_url
        }
    new_product = await ProductCRUD.add_object(session, **product_data)
    if not new_product:
        await remove_file_from_minio(image_url.split("/")[-1])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return new_product


@router.get('', response_model=List[ProductRead])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_getter)
):
    products: Optional[list[Product]] = await ProductCRUD.get_all_objects(session)
    return products

@router.get('/me', response_model=List[ProductRead])
async def get_my_products(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user)
):
    products: Optional[list[Product]] = await ProductCRUD.get_all_objects(session, seller_id=user.id)
    return products


@router.get('/{product_id}', response_model=ProductRead)
async def get_product(product_id: int, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(current_optional_user)):
    product: Optional[Product] = await ProductCRUD.get_object(session, id=product_id)
    if product and user and user.id != product.seller_id:
        veiws: Optional[ProductViews] = await ViewsCRUD.add_object(session, product_id=product_id, user_id=user.id)
        if not veiws:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при работе с бд",
            )
    return product

@router.get('/{product_id}/image')
async def get_product_image(product_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    product: Optional[Product] = await ProductCRUD.get_object(session, id=product_id)
    if not product:
        return None
    name = product.image.split("/")[-1]
    ext = product.image.split("/")[-1]
    response = await get_object(name)
    def iter_file():
            while chunk := response.read(1024 * 1024):  # Чтение по 1 МБ
                yield chunk
            response.close()
            response.release_conn()

    return StreamingResponse(
            iter_file(),
            media_type=f"image/{ext}",
            headers={"Content-Disposition": f"inline; filename={name}"}
        )



@router.patch('/{product_id}', response_model=ProductRead)
async def update_product(
    product_id: int,
    update_data: ProductUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user)
):
    product: Optional[Product] = await ProductCRUD.get_object(session, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    if (not user.is_superuser) and (product.seller_id != user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Нет прав на изменение товара",
        )
    product = await ProductCRUD.update_object(
        session,
        update_data=update_data, 
        id=product_id
    )

    if not product: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return product


@router.delete('/{product_id}')
async def delete_product(
    product_id: int, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(current_active_user)
):
    product: Optional[Product] = await ProductCRUD.get_object(session, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    if (not user.is_superuser) and (product.seller_id != user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Нет прав на удаление товара",
        )
    await remove_file_from_minio(product.image.split("/")[-1])
    result = await ProductCRUD.delete_object(session, id=product_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return result