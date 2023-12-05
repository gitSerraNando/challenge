from typing import Union

from fastapi import FastAPI
from app.auth.routers import auth
from db.database import Base, engine

def create_database():
    Base.metadata.create_all(bind=engine)


create_database()

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
