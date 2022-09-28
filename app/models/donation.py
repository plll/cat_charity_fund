from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, ProjectDonationBase


class Donation(Base, ProjectDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)