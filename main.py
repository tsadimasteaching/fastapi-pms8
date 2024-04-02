from fastapi import FastAPI
from models import User
from typing import List
from db import init_db
from routes.user import router as userrouter
from routes.job import router as jobrouter

app = FastAPI()

user1 = User(name="Nikos", surname="Tsertos", email="nick@hua.gr")

userlist = []
userlist.append(user1)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
def test()-> List[User]:
    return userlist

@app.post("/user")
def create_user(user: User) -> User:
    userlist.append(user)
    return user

app.include_router(userrouter, prefix='/user', tags=["User"])
app.include_router(jobrouter, prefix='/job', tags=["Job"])
