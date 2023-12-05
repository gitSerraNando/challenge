from google.cloud import bigquery
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

client = bigquery.Client()


def get_db():
    """
    It creates a database connection, and then yields it to the caller. 
    The caller can then use the connection, and when it's done, the connection is closed. 

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
