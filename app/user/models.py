from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    password = Column(String)
    grant_type = Column(String, default="password")
    user_type = Column(String, default="default")
    created_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
