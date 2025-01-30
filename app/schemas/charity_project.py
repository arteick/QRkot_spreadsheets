from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.constants import (EMPTY_DESCRIPTION, FULL_AMOUNT_GT,
                                   NAME_MAX_LENGTH, NAME_MIN_LENGTH)


class CharityProjectBase(BaseModel):
    """Базовый класс для схемы благотворительного проекта."""
    description: str

    @validator('description')
    def description_cannot_be_empty(cls, value: str):
        if value == '':
            raise ValueError(EMPTY_DESCRIPTION)
        return value

    class Config:
        extra = 'forbid'


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""
    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    full_amount: int = Field(..., gt=FULL_AMOUNT_GT)


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта."""
    name: str = Field(
        None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    description: str = Field(None)
    full_amount: int = Field(None, gt=FULL_AMOUNT_GT)


class CharityProjectDB(CharityProjectCreate):
    """Схема для объекта, полученного из БД."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
