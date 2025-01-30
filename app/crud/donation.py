from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import User
from app.crud.base import CRUDDonationAndProject
from app.models import Donation


class DonationCRUD(CRUDDonationAndProject):
    """Расширение базового класса для пожертвований."""
    @staticmethod
    async def get_user_donations(
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        """
        Статический метод.
        Возвращает список всех пожертвований пользователя.
        """
        donations = await session.scalars(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.all()


donation_crud = DonationCRUD(Donation)
