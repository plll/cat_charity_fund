from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import CharityProject, User, Donation


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        select_stmt = select(Donation).where(
            Donation.fully_invested is False
        )
        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        obj_in_data['invested_amount'] = 0
        for donation in donations:
            unused_amount = donation.full_amount - donation.invested_amount
            project_need = obj_in_data['full_amount'] - obj_in_data['invested_amount']
            if unused_amount < project_need:
                setattr(donation, 'fully_invested', True)
                setattr(donation, 'invested_amount', donation.full_amount)
                setattr(donation, 'close_date', datetime.now())
                obj_in_data['invested_amount'] += unused_amount
                session.add(donation)
            elif unused_amount >= project_need:
                setattr(donation, 'invested_amount', donation.invested_amount + project_need)
                obj_in_data['invested_amount'] = obj_in_data['full_amount']
                obj_in_data['close_date'] = datetime.now()
                obj_in_data['fully_invested'] = True
                session.add(donation)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        print(db_obj.fully_invested)
        if db_obj.invested_amount == db_obj.full_amount:
            setattr(db_obj, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.now())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)