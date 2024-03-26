
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User, UserBase
router = APIRouter()

@router.get("/")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/")
async def create_user(user: UserBase, session: AsyncSession = Depends(get_session)):
    dbuser = User(name=user.name, surname=user.surname, email=user.email )
    session.add(dbuser)
    await session.commit()
    await session.refresh(dbuser)
    return dbuser
    
    
