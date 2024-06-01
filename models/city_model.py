from pydantic import BaseModel, Field


class City(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Medellín")
    department: str = Field(..., min_length=3, max_length=50, example="Antioquia")
    country: str = Field(..., min_length=3, max_length=50, example="Colombia")
