from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from db import async_session_maker
from models import Users


class BaseDAO:
    @classmethod
    async def insert(cls, id, username):
        async with async_session_maker() as session:
            stmt = insert(Users).values(telegram_id=id, username=username).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def select_all(cls):
        async with async_session_maker() as session:
            stmt = select(Users)
            result = await session.execute(stmt)
            return result.scalars().all()


