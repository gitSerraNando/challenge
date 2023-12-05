from typing import Union

from fastapi import FastAPI
from app.auth.repository.auth import auth_user
from db.database import Base, engine

def create_database():
    Base.metadata.create_all(bind=engine)


create_database()

app = FastAPI()

app.include_router(auth_user.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
