from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.token import verify_token
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

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception, db)
