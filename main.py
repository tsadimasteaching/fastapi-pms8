from fastapi import FastAPI
from models import User
from typing import List
app = FastAPI()

user1 = User(name="Nikos", surname="Tsertos", email="nick@hua.gr")

userlist = []
userlist.append(user1)

@app.get("/")
def test()-> List[User]:
    return userlist

@app.post("/user")
def create_user(user: User) -> User:
    userlist.append(user)
    return user


