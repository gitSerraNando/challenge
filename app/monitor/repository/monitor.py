from sqlite3 import IntegrityError

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.monitor.models import LogEntry
from app.monitor.schema.monitor import LogCreate


class MonitorService:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, log: LogCreate):
        new_log = LogEntry(level=log.level, message=log.message)
        try:
            self.db.add(new_log)
            self.db.commit()
            self.db.refresh(new_log)
            return new_log
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Database error: {e}"
            )
