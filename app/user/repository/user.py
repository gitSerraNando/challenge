from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.user import models
from app.utils.hashing import Hash


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        user = self.db.query(models.User).filter(
            models.User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found"
            )
        return user
