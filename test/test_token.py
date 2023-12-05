import pytest
from datetime import datetime, timedelta
from app.utils.token import JWTService, TokenData

class MockUser:
    def __init__(self, email, user_type):
        self.email = email
        self.user_type = user_type


class MockDB:
    def get_user_by_email(self, email):
        if email == "test@example.com":
            return MockUser(email=email, user_type="admin")
        return None

    def query(self, *args, **kwargs):
        # Simula el comportamiento del método 'query' de SQLAlchemy
        class MockQuery:
            def filter(self, *args, **kwargs):
                # Esta función ahora devuelve una instancia de MockQuery
                return self

            def first(self):
                # Devuelve un MockUser o None dependiendo del email
                if "test@example.com" in str(args):
                    return MockUser(email="test@example.com", user_type="admin")
                return None

        return MockQuery()




@pytest.fixture
def jwt_service():
    return JWTService()

@pytest.fixture
def mock_db():
    return MockDB()


def test_create_access_token(jwt_service):
    data = {"sub": "test@example.com", "user_type": "admin"}
    token = jwt_service.create_access_token(data)
    assert isinstance(token, str)

def test_verify_token_valid(jwt_service, mock_db):
    data = {"sub": "test@example.com", "user_type": "admin"}
    token = jwt_service.create_access_token(data)
    token_data = jwt_service.verify_token(token, ValueError, mock_db)
    assert isinstance(token_data, TokenData)
    assert token_data.email == "test@example.com"
    assert token_data.user_type == "admin"

def test_verify_token_invalid(jwt_service, mock_db):
    token = "invalid_token"
    with pytest.raises(ValueError):
        jwt_service.verify_token(token, ValueError, mock_db)

def test_verify_basic_token_valid(jwt_service):
    data = {"sub": "test@example.com", "user_type": "admin"}
    token = jwt_service.create_access_token(data)
    token_data = jwt_service.verify_basic_token(token)
    assert isinstance(token_data, TokenData)
    assert token_data.email == "test@example.com"
    assert token_data.user_type == "admin"

def test_verify_basic_token_expired(jwt_service):
    data = {"sub": "test@example.com", "user_type": "admin"}
    expire = datetime.utcnow() - timedelta(minutes=30)
    data["exp"] = expire
    token = jwt_service.create_access_token(data)
    with pytest.raises(ValueError):
        jwt_service.verify_basic_token(token)

        jwt_service.verify_basic_token(token)

def test_verify_basic_token_invalid(jwt_service):
    token = "invalid_token"
    with pytest.raises(ValueError):
        jwt_service.verify_basic_token(token)