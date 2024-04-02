from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User, UserBase, Job, JobBase
from typing import List
router = APIRouter()

@router.get("/", response_model=List[Job])
async def list_jobs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


@router.post("/")
async def create_job(job: JobBase, session: AsyncSession = Depends(get_session)):
    dbjob = Job(title=job.title, description=job.description, company=job.company, user_id=job.user_id )
    session.add(dbjob)
    await session.commit()
    await session.refresh(dbjob)
    return dbjob
