from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CreateAuthor(BaseModel):
    name: str
    bio: str
    birthdate: str

    class Config:
        orm_mode = True

    def parsed_datetime(self) -> datetime:
        return datetime.fromisoformat(self.birthdate)


class UpdateAuthor(BaseModel):
    id: int
    name: str
    bio: str
    birthdate: str

    class Config:
        orm_mode = True

    def parsed_datetime(self) -> datetime:
        return datetime.fromisoformat(self.birthdate)

class Author(BaseModel):
    id: int
    name: str
    bio: str
    birthdate: str = ""

class GetAuthorRequest(BaseModel):
    name: Optional[str] = ""
    page: Optional[int] = 1
    pageSize: Optional[int] = 10


class GetAuthorResponse(BaseModel):
    authors: List[Author]
    page: int
    pageSize: int
    total: int
