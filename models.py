from sqlalchemy import BigInteger, Column, String
from db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String)
