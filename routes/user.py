
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User, UserBase, UserwithJobs
from typing import List, Union
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("/", response_model=List[User])
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/", response_model=User)
async def create_user(user: UserBase, session: AsyncSession = Depends(get_session)):
    dbuser = User(name=user.name, surname=user.surname, email=user.email )
    session.add(dbuser)
    await session.commit()
    await session.refresh(dbuser)
    return dbuser

@router.get("/{user_id}", response_model=UserwithJobs)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id).options(selectinload(User.jobs)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserBase, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    dbuser = result.scalars().first()
    if not dbuser:
        raise HTTPException(status_code=404, detail="User not found")
    dbuser.name = user.name
    dbuser.surname = user.surname
    dbuser.email = user.email
    await session.commit()
    return dbuser
    
@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    dbuser = result.scalars().first()
    if not dbuser:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(dbuser)
    await session.commit()
    return  {"ok": "user deleted"}