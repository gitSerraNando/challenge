import pytest
from app.utils.hashing import Hash

class TestHash:
    @pytest.fixture(scope="class")
    def hash_obj(self):
        return Hash()

    def test_hash_password(self, hash_obj):
        password = "password123"
        hashed_password = hash_obj.hash_password(password)
        assert isinstance(hashed_password, str)
        assert hashed_password != password

    def test_verify_password_valid(self, hash_obj):
        password = "password123"
        hashed_password = hash_obj.hash_password(password)
        assert hash_obj.verify_password(password, hashed_password) is True

    def test_verify_password_invalid(self, hash_obj):
        password = "password123"
        hashed_password = hash_obj.hash_password(password)
        assert hash_obj.verify_password("wrong_password", hashed_password) is False
