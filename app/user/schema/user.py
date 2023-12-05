from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(...)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "test@dominio.com"
            }
        }


class User(UserBase):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Hernando",
                "last_name": "Escobar"
            }
        }


class UserCreate(User):
    password: str = Field(..., min_length=8, max_length=60)
    user_type: str = Field(...)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "password": "12345678",
                "user_type": "Admin"
            }
        }


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
