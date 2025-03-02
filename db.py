from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_HOST, DB_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
