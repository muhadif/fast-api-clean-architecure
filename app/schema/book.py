from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schema.author import Author


class CreateBook(BaseModel):
    title: str
    description: str
    publish_date: str
    author_id: int

    def parsed_datetime(self) -> datetime:
        return datetime.fromisoformat(self.publish_date)


class UpdateBook(BaseModel):
    id: int
    title: str
    description: str
    publish_date: str
    author_id: int

    def parsed_datetime(self) -> datetime:
        return datetime.fromisoformat(self.publish_date)

class Book(BaseModel):
    id: int
    title: str
    description: str
    publish_date: str
    author_id: int
    author: Author

class GetBookRequest(BaseModel):
    author_id: Optional[int] = 0
    page: Optional[int] = 1
    pageSize: Optional[int] = 10


class GetBookResponse(BaseModel):
    books: List[Book]
    page: int
    pageSize: int
    total: int
