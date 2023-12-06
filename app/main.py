from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.auth.routers import auth
from app.employee.routers import employee
from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from app.product.routers import product
from db.database import Base, engine, SessionLocal

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


@app.middleware("http")
async def log_requests_responses(request: Request, call_next):
    response = await call_next(request)
    db = SessionLocal()
    try:
        monitor_service = MonitorService(db)
        log_data = LogCreate(
            level=LogsType.INFO.value,
            message=f"Request: {request.url} - Response: {response.status_code}"
        )
        monitor_service.create_log(log_data)
        db.commit()
    finally:
        db.close()
    return response


app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(product.router)

add_pagination(app)
