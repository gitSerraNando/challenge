from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.repository.auth import AuthService
from app.auth.schema.auth import TokenResponse
from app.user.repository.user import UserService
from app.user.schema.user import UserCreate, UserResponse
from db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Register a User",
)
async def signup(user_body: UserCreate = Body(...), db: Session = Depends(get_db)):
    """
    Register a new user.

    Parameters:
    - user_body: UserCreate - The user details for registration.
    
    Returns:
    - UserResponse: The registered user's public information.
    """
    user_service = UserService(db)
    return user_service.create_user(user_body)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    summary="Login a User"
)
async def login(user: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    """
    Authenticate a user and provide an access token.

    Parameters:
    - user: OAuth2PasswordRequestForm - The user's login credentials.
    
    Returns:
    - TokenResponse: Access token for the authenticated user.
    """
    auth_service = AuthService(db)
    auth_token = auth_service.authenticate_user(user)
    return auth_token
