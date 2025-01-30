from datetime import datetime
from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс. Предоставляет все операции CRUD"""
    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Optional[ModelType]:
        """Возвращает объект по id."""
        return await session.get(self.model, obj_id)

    async def get_all(
            self,
            session: AsyncSession
    ) -> list[ModelType]:
        """Возвращает все объекты."""
        model_obj_list = await session.scalars(
            select(self.model)
        )
        return model_obj_list.all()

    async def create(
            self,
            data: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        """Записывает объект в БД."""
        obj_data = data.dict()
        if user is not None:
            obj_data['user_id'] = user.id
        obj = self.model(**obj_data)
        session.add(obj)
        return await CRUDBase.commit_and_refresh(obj, session)

    async def update(
            self, obj: ModelType,
            data: UpdateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        """Обновляет объект в БД."""
        fields = jsonable_encoder(obj)
        updated_data = data.dict(exclude_unset=True)
        for field in fields:
            if field in updated_data:
                setattr(obj, field, updated_data[field])
        session.add(obj)
        return await CRUDBase.commit_and_refresh(obj, session)

    async def remove(
            self,
            obj: ModelType,
            session: AsyncSession
    ) -> ModelType:
        """Удаляет объект в БД."""
        await session.delete(obj)
        await session.commit()
        return obj

    @staticmethod
    async def commit_and_refresh(
        obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        """Фиксирует изменения за сессию и обновляет объект модели."""
        await session.commit()
        await session.refresh(obj)
        return obj


class CRUDDonationAndProject(CRUDBase):
    """Базовый класс для пожертвований и проектов."""

    @staticmethod
    async def close_obj(
        obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        """
        Статический метод.
        Закрывает проект/пожертвование.
        Метод session.commit() не вызывается.
        """
        obj.close_date = datetime.now()
        obj.fully_invested = True
        session.add(obj)
        return obj

    @staticmethod
    async def get_partially_donated(
        model: ModelType,
        session: AsyncSession
    ) -> Optional[list[ModelType]]:
        """
        Возвращает список непотраченных пожертвований или открытых
        проектов в зависимости от указанной модели.
        """
        objects = await session.scalars(
            select(model).where(
                model.fully_invested == 0
            ).order_by(model.create_date)
        )
        return objects.all()