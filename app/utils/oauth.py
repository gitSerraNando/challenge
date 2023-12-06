from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from app.utils.token import JWTService
from db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    It takes a token, and if it's valid, it returns the user associated with that token.
    :param token: str = Depends(oauth2_scheme)
    :type token: str
    :param db: Session = Depends(get_db)
    :type db: Session
    :return: The user object
    """
    monitor_service = MonitorService(db)
    log_data = LogCreate(level=LogsType.WARNING,
                         message=f"Detail: Could not validate credentials - Response: {status.HTTP_401_UNAUTHORIZED}")
    monitor_service.create_log(log_data)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    jwt_service = JWTService()
    return jwt_service.verify_token(token, credentials_exception, db)
