from sqlalchemy.dialects.postgresql import insert
from db import async_session_maker
from models import Users


class BaseDAO:
    @classmethod
    async def insert(cls, id):
        async with async_session_maker() as session:
            stmt = insert(Users).values(telegram_id=id).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()


