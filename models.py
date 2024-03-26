from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=20)
    surname: str = Field()
    email: str = Field()

