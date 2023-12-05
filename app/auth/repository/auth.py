from sqlalchemy.orm import Session
from app.user import models
from fastapi import HTTPException, status
from app.user.repository.user import UserService
from app.utils.hashing import Hash
from app.utils.token import JWTService

RESPONSE = """Incorrect user or password please retry!"""


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, user_request):
        """
        Authenticate a user based on email and password.

        Args:
            user_request: The request containing the username and password.

        Returns:
            dict: Access token information if authentication is successful.

        Raises:
            HTTPException: If authentication fails.
        """
        user_service = UserService(self.db)
        try:
            user = user_service.get_user_by_email(email=user_request.username)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=RESPONSE
            )
        self._verify_password(user_request.password, user.password)
        access_token = self._create_access_token(user)
        return {"access_token": access_token, "token_type": "bearer"}

    def _verify_password(self, plain_password, hashed_password):
        hasher = Hash()
        if not hasher.verify_password(plain_password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect user or password please retry!"
            )

    def _create_access_token(self, user):
        jwt_service = JWTService()
        return jwt_service.create_access_token(
            data={"sub": user.email, "user_type": user.user_type}
        )
