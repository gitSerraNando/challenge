import jwt
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from app.auth.schema.auth import TokenData
from core.config import settings
from app.user.repository.user import UserService


class JWTService:
    """
    Service class for handling JSON Web Tokens (JWT).

    Attributes:
        secret_key (str): The secret key used for token encoding and decoding.
        algorithm (str): The algorithm used for token encoding and decoding.
        access_token_expire_minutes (int): The expiration time of access tokens in minutes.

    Methods:
        create_access_token(data: dict) -> str: Creates an access token based on the provided data.
        verify_token(token: str, credentials_exception, db) -> TokenData: Verifies the validity of a token and returns the corresponding user data.
        verify_basic_token(token: str) -> TokenData: Verifies the validity of a basic token and returns the corresponding user data.
    """

    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict) -> str:
        """
        Creates an access token based on the provided data.

        Args:
            data (dict): The data to be encoded in the token.

        Returns:
            str: The generated access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, credentials_exception, db) -> TokenData:
        """
        Verifies the validity of a token and returns the corresponding user data.

        Args:
            token (str): The token to be verified.
            credentials_exception: The exception to be raised if the token is invalid.
            db: The database connection object.

        Returns:
            TokenData: The user data extracted from the token.

        Raises:
            credentials_exception: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email = payload.get("sub")
            user_type = payload.get("user_type")

            if email is None or user_type is None:
                raise credentials_exception
            user_service = UserService(db)

            db_user = user_service.get_user_by_email(email=email)
            if db_user is None or db_user.email != email or db_user.user_type != user_type:
                raise credentials_exception

            return TokenData(email=email, user_type=user_type)

        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except InvalidTokenError:
            raise ValueError from None
        except PyJWTError:
            raise ValueError from None

    def verify_basic_token(self, token: str) -> TokenData:
        """
        Verifies the validity of a basic token and returns the corresponding user data.

        Args:
            token (str): The token to be verified.

        Returns:
            TokenData: The user data extracted from the token.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email = payload.get("sub")
            user_type = payload.get("user_type")
            return TokenData(email=email, user_type=user_type)

        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except InvalidTokenError:
            raise ValueError("Invalid token")
        except PyJWTError:
            raise ValueError("Error processing token")
