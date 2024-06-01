from typing import Optional

from pydantic import BaseModel, Field

from models.city_model import City


class Location(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Aula de informática")
    address: str = Field(..., min_length=3, max_length=50, example="P13-211")
    city: City

