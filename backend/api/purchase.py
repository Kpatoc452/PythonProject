from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from api.Dependencies.fastapi_users_object import current_active_user
from core.schemas.product import ProductUpdate
from core.models.db_helper import db_helper
from core.models.user import User
from core.models import Product
from crud.products import ProductCRUD
from crud.purchase import PurchaseCRUD

router = APIRouter(
    prefix="/purchase",
    tags=["Purchase"],
)

@router.post('/{product_id}')
async def create_purchase(
    product_id: int, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(current_active_user)
):
    product: Optional[Product] = await ProductCRUD.get_object(session, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    if product.sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Товар уже продан",
        )
    if user.id == product.seller_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя купить собственный товар",
        )
    purchase_data = {
        "user_id": user.id,
        "product_id": product_id
    }
    update_data: ProductUpdate = ProductUpdate(sold=True)

    product_update: Optional[Product] = await ProductCRUD.update_object(session, update_data=update_data, id=product.id)
    if not product_update:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    new_purchase = await PurchaseCRUD.add_object(session, **purchase_data)
    if not new_purchase:
        update_data: ProductUpdate = ProductUpdate(sold=False)
        _: Optional[Product] = await ProductCRUD.update_object(session, update_data=update_data, id=product.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд, покупка не завершена",
        )
    return new_purchase