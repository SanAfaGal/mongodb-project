from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, Field

from models.location_model import Location


class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, example="Maratón de BD")
    description: str = Field(..., min_length=10, max_length=500,
                             example="Participación en una serie de desafíos "
                                     "relacionados con la gestión y el análisis de datos.")
    categories: List[str] = Field(..., min_items=1, max_items=10, example=["Programación", "Maratón BD"])
    date: datetime = Field(..., example=datetime(2019, 9, 7))
    location: Location
    organizers: List[str] = Field(..., min_items=1, max_items=10,
                                  example=["Facultad de Ingeniería", "Programa de Ingeniería Informática"])
    attendees: Optional[List[Any]] = Field(..., min_items=0, max_items=1000, example=[""])
    speakers: List[Any] = Field(..., min_items=0, max_items=100, example=[""])


class Event(EventCreate):
    id: Optional[str] = Field(alias="_id")


class EventShow(Event):
    comments: Optional[List[Any]] = Field(..., min_items=0, max_items=100)
