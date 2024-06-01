from typing import Optional

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=100, example="¡Super!")
    user_id: str = Field(min_length=24, max_length=24, example="")
    event_id: str = Field(min_length=24, max_length=24, example="")


class Comment(CommentCreate):
    id: Optional[str] = Field(alias="_id")
