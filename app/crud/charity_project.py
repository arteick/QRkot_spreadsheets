from typing import Optional

from sqlalchemy import select, extract, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDDonationAndProject
from app.models import CharityProject


class CharityProjectCRUD(CRUDDonationAndProject):
    """Расширение базового класса для благотворительных проектов."""
    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[CharityProject]:
        projects = await session.scalars(
            select(
                CharityProject.name,
                extract(
                    text('DAY_SECOND'),
                    CharityProject.close_date -
                    CharityProject.create_date
                ).label('time'),
                CharityProject.description
            ).where(
                CharityProject.fully_invested == 1
            ).order_by('time')
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
