from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Login(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="yourpassword")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsIn...")
    token_type: str = Field(default="bearer", example="bearer")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    email: Optional[EmailStr] = Field(default=None, example="user@example.com")
    user_type: Optional[str] = Field(default=None, example="admin")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "user_type": "admin"
            }
        }

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsIn...")
    token_type: str = Field(default="bearer", example="bearer")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
                "token_type": "bearer"
            }
        }
