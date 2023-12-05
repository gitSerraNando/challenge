from sqlite3 import IntegrityError

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from app.user import models
from app.user.schema.user import UserCreate
from app.utils.hashing import Hash


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        user = self.db.query(models.User).filter(
            models.User.email == email).first()
        if not user:
            monitor_service = MonitorService(self.db)
            log_data = LogCreate(level=LogsType.WARNING,
                                 message=f"Detail: get_user_by_email :User with email {email} not found - Response: {status.HTTP_404_NOT_FOUND}")
            monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found"
            )
        return user

    def create_user(self, user: UserCreate):
        """
        Create a new user in the database.

        Args:
            user (UserCreate): The user data transfer object containing user information.

        Returns:
            models.User: The created user object.

        Raises:
            HTTPException: If the user already exists or if there is a database error.
        """
        existing_user = self.db.query(
            models.User).filter_by(email=user.email).first()
        if existing_user:
            monitor_service = MonitorService(self.db)
            log_data = LogCreate(level=LogsType.WARNING,
                                 message=f"Detail: create_user :Email already registered. - Response: {status.HTTP_409_CONFLICT}")
            monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered."
            )

        hashed_password = Hash().hash_password(user.password)
        new_user = models.User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hashed_password,
            user_type=user.user_type
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            self.db.rollback()
            monitor_service = MonitorService(self.db)
            log_data = LogCreate(level=LogsType.ERROR,
                                 message=f"Detail: create_user :Database error: {e} - Response: {status.HTTP_500_INTERNAL_SERVER_ERROR}")
            monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}"
            )
