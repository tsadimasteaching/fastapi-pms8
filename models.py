from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, String

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(sa_column=Column(String(30)))
    surname: str = Field()
    email: str = Field()
