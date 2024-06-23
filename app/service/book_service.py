from typing import List

from app.model.model import Book
from app.repository.book_repository import BookRepository
from app.schema.book import CreateBook, UpdateBook, GetBookRequest


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get(self, req: GetBookRequest):
        return self.book_repository.get(req)

    def get_by_id(self, id):
        return self.book_repository.get_by_id(id)

    def create(self, req: CreateBook):
        book = Book(**req.model_dump())
        return self.book_repository.create(book)

    def update(self, req: UpdateBook):
        book = Book(**req.model_dump())
        return self.book_repository.update(book)

    def delete(self, id):
        return self.book_repository.delete(id)

    def delete_by_author_id(self, id):
        return self.book_repository.delete(id)
