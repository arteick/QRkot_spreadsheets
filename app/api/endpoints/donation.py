from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDBSuperUser, DonationDBUser
from app.services.donation import distribute_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=list[DonationDBUser]
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_user_donations(session, user)


@router.post(
    '/',
    response_model=DonationDBUser
)
async def create_donation(
    data: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    donation = await donation_crud.create(data, session, user)
    return await distribute_donation(donation, session)
