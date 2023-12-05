from typing import Union

from fastapi import FastAPI
from app.auth.routers import auth
from db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
]

description = """
Celes API  Challenge. 🚀

# Prueba Técnica Backend Python
## Datamart:

"""

def create_database():
    Base.metadata.create_all(bind=engine)


create_database()

app = FastAPI(
    title="Celes",
    description=description,
    version="0.0.1",
    contact={
        "name": "Hernando Escobar",
        "url": "https://github.com/gitSerraNando/challenge-datamart",
        "email": "hernandoescobar23@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


