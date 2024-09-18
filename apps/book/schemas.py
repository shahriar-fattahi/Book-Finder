from typing import ClassVar, List, Union

from pydantic import BaseModel, Field

from apps.users.schemas import User as UserSchema

from .managers import BookManager


class Review(BaseModel):
    id: int = Field(gt=0)
    book: Union[int, "Book"]
    user: Union[int, UserSchema]
    rating: int = Field(ge=1, le=5)


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    genre: str = Field(max_length=255)
    reviews: List[Review] = Field(default=[])

    objects: ClassVar["BookManager"] = BookManager(db_table_name="books")

    def __str__(self) -> str:
        return self.title
