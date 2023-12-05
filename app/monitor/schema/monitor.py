from enum import Enum

from pydantic import BaseModel, Field


class LogsType(str, Enum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'


class LogCreate(BaseModel):
    level: str = Field(...)
    message: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "level": LogsType.INFO,
                "message": "This is a test message"
            }
        }
