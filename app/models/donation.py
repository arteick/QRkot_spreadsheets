from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):
    """Модель для таблицы пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
