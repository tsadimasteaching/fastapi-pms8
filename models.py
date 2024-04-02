from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, String, Relationship
from typing import List, ForwardRef

UserwithJobs = ForwardRef('UserwithJobs')
JobwithUser = ForwardRef('JobwithUser')

class UserBase(SQLModel):
    name: str = Field()
    surname: str = Field()
    email: str = Field()
    
class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    jobs: List["Job"] = Relationship(back_populates="user")


class UserwithJobs(UserBase):
    id : int
    jobs: List["Job"] = []

class JobBase(SQLModel):
    title: str = Field()
    description: str = Field()
    company: str = Field()
    user_id: int = Field(foreign_key="user.id")


class Job(JobBase, table=True):
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="jobs")

class JobwithUser(JobBase):
    id: int
    user: UserBase
class JobCreate(JobBase):
    pass


UserwithJobs.update_forward_refs()
JobwithUser.update_forward_refs()
