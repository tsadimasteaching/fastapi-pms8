
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

@router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return user

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserBase, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    dbuser = result.scalars().first()
    print(f"User: {dbuser}")
    dbuser.name = user.name
    dbuser.surname = user.surname
    dbuser.email = user.email
    await session.commit()
    return dbuser
    
@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    dbuser = result.scalars().first()
    print(f"User: {dbuser}")
    await session.delete(dbuser)
    await session.commit()
    return dbuser