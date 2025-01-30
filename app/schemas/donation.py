from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    """Схема для создания пожертвования."""
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationDBUser(DonationCreate):
    """
    Схема для пожертвования, полученного из БД обычным пользователем.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperUser(DonationDBUser):
    """
    Схема для пожертвования, полученного из БД суперпользователем.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
