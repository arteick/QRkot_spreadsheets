from sqlalchemy import Column, String, Text

from app.models.base import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    """Модель для таблицы благотворительных проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text(200), nullable=False)
