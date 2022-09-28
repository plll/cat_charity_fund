from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User, CharityProject


class CRUDDonation(CRUDBase):

    async def get_my_donations(
            self,
            user_id: int,
            session: AsyncSession
    ) -> list[Donation]:
        select_stmt = select(Donation).where(
            Donation.user_id == user_id
        )
        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        return donations

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        select_stmt = select(CharityProject).where(
            CharityProject.fully_invested is False
        )
        projects = await session.execute(select_stmt)
        projects = projects.scalars().all()
        obj_in_data['invested_amount'] = 0
        for project in projects:
            unused_amount = obj_in_data['full_amount'] - obj_in_data['invested_amount']
            project_need = project.full_amount - project.invested_amount
            if unused_amount == 0:
                break
            elif unused_amount >= project_need:
                setattr(project, 'fully_invested', True)
                setattr(project, 'invested_amount', project.full_amount)
                setattr(project, 'close_date', datetime.now())
                obj_in_data['invested_amount'] += project_need
                session.add(project)
            elif unused_amount < project_need:
                setattr(project, 'invested_amount', project.invested_amount + unused_amount)
                obj_in_data['invested_amount'] = obj_in_data['full_amount']
                obj_in_data['close_date'] = datetime.now()
                obj_in_data['fully_invested'] = True
                session.add(project)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


donation_crud = CRUDDonation(Donation)