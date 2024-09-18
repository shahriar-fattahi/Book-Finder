from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(gt=0)
    username: str = Field(max_length=50)
