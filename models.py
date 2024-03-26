from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, String


class UserBase(SQLModel):
    name: str = Field()
    surname: str = Field()
    email: str = Field()
    
class User(UserBase, table=True):
    id: int = Field(primary_key=True)

