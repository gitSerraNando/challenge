import pytest
from datetime import datetime, timedelta
from app.utils.token import JWTService, TokenData
from logging import raiseExceptions
import pytest
from app.user.repository.user import UserService
from app.user.schema.user import UserCreate
from app.utils.hashing import Hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


TEST_EMAIL = "test@example.com"

class MockDB:
    def __init__(self):
        self.users = []
    def add(self, user):
        self.users.append(user)

    def commit(self):
        pass

    def refresh(self,user):
        self.users.append(user)

    def rollback(self):
        pass

    class MockQuery:
        def __init__(self, users):
            self.users = users

        def filter(self, *filters):
            # Implementación simplificada del filtro
            filtered_users = [user for user in self.users if all(getattr(user, str(arg.left).split('.')[1]) == arg.right for arg in filters)]
            return MockFilterQuery(filtered_users)

        def filter_by(self, **kwargs):
            filtered_users = [user for user in self.users if all(getattr(user, key) == value for key, value in kwargs.items())]
            return MockFilterQuery(filtered_users)

        def all(self):
            # Retorna todos los usuarios en caso de que se llame a `all()`
            return self.users

    def query(self, *args):
        return self.MockQuery(self.users)

class MockFilterQuery:
    def __init__(self, filtered_users):
        self.filtered_users = filtered_users

    def first(self):
        return self.filtered_users[0] if self.filtered_users else None

    def all(self):
        return self.filtered_users




@pytest.fixture
def user_repository():
    return UserService(MockDB())

@pytest.fixture
def jwt_service():
    return JWTService()

@pytest.fixture
def mock_db():
    return MockDB()



def test_create_user_success(user_repository):
    user_data = UserCreate(
        email=TEST_EMAIL,
        first_name="John",
        last_name="Doe",
        password="password",
        user_type="Admin"
    )

    existing_user = UserCreate(
        email="existing@example.com",
        first_name="Existing",
        last_name="User",
        password="password",
        user_type="Admin"
    )
    user_repository.db.add(existing_user)

    user = user_repository.create_user(user_data)

    assert user.email == TEST_EMAIL
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert Hash().verify_password("password", user.password)
    assert user.user_type == "Admin"



def test_create_user_existing_email(user_repository):
    user_data = UserCreate(
        email=TEST_EMAIL,
        first_name="John",
        last_name="Doe",
        password="password",
        user_type="Admin"
    )
    user_repository.db.users.append(user_data)
    with pytest.raises(HTTPException) as e:
        user_repository.create_user(user_data)
    assert e.value.status_code == status.HTTP_409_CONFLICT
    assert e.value.detail == "Email already registered."
def test_create_access_token(jwt_service):
    data = {"sub": TEST_EMAIL, "user_type": "Admin"}
    token = jwt_service.create_access_token(data)
    assert isinstance(token, str)


def test_verify_token_invalid(jwt_service, mock_db):
    token = "invalid_token"
    with pytest.raises(ValueError):
        jwt_service.verify_token(token, ValueError, mock_db)

def test_verify_basic_token_valid(jwt_service):
    data = {"sub": TEST_EMAIL, "user_type": "Admin"}
    token = jwt_service.create_access_token(data)
    token_data = jwt_service.verify_basic_token(token)
    assert isinstance(token_data, TokenData)
    assert token_data.email == TEST_EMAIL
    assert token_data.user_type == "Admin"



def test_verify_basic_token_invalid(jwt_service):
    token = "invalid_token"
    with pytest.raises(ValueError):
        jwt_service.verify_basic_token(token)