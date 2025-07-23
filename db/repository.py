from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import HistoryModel


class Repository:
    def __init__(self, session: AsyncSession):
        self.session =  session


    async def save(self, address: str) -> bool:
        try:
            new_record = HistoryModel(address=address)
            self.session.add(new_record)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Database save error: {str(e)}")

    async def get_history(self, limit: int):
        try:
            query = select(HistoryModel).offset(0).limit(limit)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise ValueError(f"Database query error: {str(e)}")
