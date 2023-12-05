from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(default="bearer")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    user_type: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "user_type": "admin"
            }
        }


class TokenResponse(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(default="bearer")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
                "token_type": "bearer"
            }
        }
