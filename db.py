import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
load_dotenv()

DATABASE_URL = os.environ.get("DB_URL")

print(f'DATABASE URL is {DATABASE_URL}')

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker (engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)