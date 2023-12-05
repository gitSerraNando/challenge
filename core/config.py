import os
from pathlib import Path

env_path = Path('.') / '.env'


class Settings:
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


settings = Settings()
