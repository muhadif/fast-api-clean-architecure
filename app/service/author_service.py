from typing import List

from app.model.model import Author
from app.repository.author_repository import AuthorRepository
from app.repository.book_repository import BookRepository
from app.schema.author import CreateAuthor, UpdateAuthor, GetAuthorRequest


class AuthorService:
    def __init__(self, author_repository: AuthorRepository, book_repository: BookRepository):
        self.author_repository = author_repository
        self.book_repository = book_repository

    def get(self, req: GetAuthorRequest):
        return self.author_repository.get(req)

    def get_by_id(self, id):
        return self.author_repository.get_by_id(id)

    def create(self, req: CreateAuthor):
        author = Author(**req.dict())
        author.birthdate = req.parsed_datetime()
        return self.author_repository.create(author)

    def update(self, req: UpdateAuthor):
        author = Author(**req.dict())
        author.birthdate = req.parsed_datetime()
        return self.author_repository.update(author)

    def delete(self, id):
        self.book_repository.delete_by_author_id(id)
        return self.author_repository.delete(id)
