from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

class BaseCRUD:

    model = None

    @classmethod
    async def get_object(cls, session: AsyncSession, **kwargs):
        try:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
        except SQLAlchemyError as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return result.mappings().one_or_none()

    @classmethod
    async def get_all_objects(cls, session: AsyncSession, **kwargs):
        try:
            query = (select(cls.model.__table__.columns)
                .filter_by(**kwargs)
                .order_by(cls.model.id))
            result = await session.execute(query)
        except (SQLAlchemyError, Exception) as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return result.mappings().all()

    @classmethod
    async def add_object(cls, session: AsyncSession, **kwargs):
        try:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return 'Данные успешно добавлены.'

    @classmethod
    async def add_objects(cls, session: AsyncSession, **data):
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return result.mappings().first()

    @classmethod
    async def update_object(cls, session: AsyncSession, update_data, **kwargs):
        """Позволяет обновлять данные объекта."""
        try:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            new_data = update_data.dict(exclude_unset=True)

            for key, value in new_data.items():
                setattr(result, key, value)
            session.add(result)
            await session.commit()
            await session.refresh(result)
        except (SQLAlchemyError, Exception) as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return result

    @classmethod
    async def delete_object(cls, session: AsyncSession, **kwargs):
        try:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            await session.delete(result)
            await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'Произошла ошибка: {error}'
            logger.error(message)
            return None
        return 'Удаление успешно завершено.'