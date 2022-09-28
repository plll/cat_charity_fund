from sqlalchemy import Column, String

from app.core.db import ProjectDonationBase, Base


class CharityProject(ProjectDonationBase, Base):
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
