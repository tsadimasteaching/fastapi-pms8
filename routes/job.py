from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User, UserBase, Job, JobBase, JobwithUser
from typing import List
from sqlalchemy.orm import selectinload
router = APIRouter()

@router.get("/", response_model=List[Job])
async def list_jobs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


@router.post("/", response_model=Job)
async def create_job(job: JobBase, session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User).filter(User.id == job.user_id))
    if not user.scalars().first():
        raise HTTPException(status_code=404, detail="User not found")
    dbjob = Job(title=job.title, description=job.description, company=job.company, user_id=job.user_id )
    session.add(dbjob)
    await session.commit()
    await session.refresh(dbjob)
    return dbjob

@router.get("/{job_id}", response_model=JobwithUser)
async def get_job(job_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job).filter(Job.id == job_id).options(selectinload(Job.user)))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
