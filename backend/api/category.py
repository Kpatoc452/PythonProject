from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from api.Dependencies.fastapi_users_object import current_superuser
from core.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from core.models.db_helper import db_helper
from core.models.user import User
from core.models.categories import Category
from crud.categories import CategoryCRUD

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)

@router.post('')
async def create_category(
    data: CategoryCreate, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(current_superuser)
):
    new_category = await CategoryCRUD.add_object(session, **data.model_dump())

    if not new_category:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return new_category


@router.get('', response_model=List[CategoryRead])
async def get_categories(
    session: AsyncSession = Depends(db_helper.session_getter)
):
    categories: Optional[list[Category]] = await CategoryCRUD.get_all_objects(session)

    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return categories

@router.get('/{category_id}', response_model=CategoryRead)
async def get_category(category_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    category: Optional[Category] = await CategoryCRUD.get_object(session, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return category


@router.patch('/{category_id}', response_model=CategoryRead)
async def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_superuser)
):
    category = await CategoryCRUD.update_object(
        session,
        update_data=update_data, 
        id=category_id
    )

    if not category: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return category


@router.delete('/{category_id}')
async def delete_category(
    category_id: int, session: AsyncSession = Depends(db_helper.session_getter), user: User = Depends(current_superuser)
):
    result = await CategoryCRUD.delete_object(session, id=category_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при работе с бд",
        )
    return result

