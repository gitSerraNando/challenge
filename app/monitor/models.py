from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from db.database import Base


class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
