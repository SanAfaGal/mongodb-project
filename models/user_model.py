from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from models.city_model import City


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    full_name: str = Field(..., min_length=3, max_length=100, example="John Doe")
    relationship: str = Field(..., min_length=3, max_length=50, example="Professor")
    email: EmailStr = Field(..., example="john.doe@example.com")
    city: City


class User(UserCreate):
    id: Optional[str] = Field(alias="_id")
