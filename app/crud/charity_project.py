from typing import Optional

from sqlalchemy import func, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDDonationAndProject
from app.models import CharityProject


class CharityProjectCRUD(CRUDDonationAndProject):
    """Расширение базового класса для благотворительных проектов."""
    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[CharityProject]:
        projects = await session.execute(
            select(
                CharityProject.name,
                (
                    func.printf(
                        "%d days, %02d:%02d:%02d.%d",
                        (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                        ),  # дни с дробной частью
                        (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                        ) * 24 % 24,  # часы
                        (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                        ) * 1440 % 60,  # минуты
                        (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                        ) * 86400 % 60,  # секунды
                        (
                            func.julianday(CharityProject.close_date) -
                            func.julianday(CharityProject.create_date)
                        ) * 86400000 % 1000  # милисекунды
                    )
                ).label('time'),
                CharityProject.description
            ).where(
                CharityProject.fully_invested == true()
            ).order_by(
                (
                    func.strftime('%s', CharityProject.close_date) -
                    func.strftime('%s', CharityProject.create_date)
                )
            )
        )
        return projects.all()

    @staticmethod
    async def get_id_by_name(
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Статический метод. Возвращает id проекта по имени."""
        charity_project_id = await session.scalars(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project_id.first()


charity_project_crud = CharityProjectCRUD(CharityProject)
