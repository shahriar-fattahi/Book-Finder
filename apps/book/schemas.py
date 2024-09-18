from typing import ClassVar

from pydantic import BaseModel, Field

from .managers import BookManager


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    genre: str = Field(max_length=255)

    objects: ClassVar["BookManager"] = BookManager(db_table_name="books")

    def __str__(self) -> str:
        return self.title
