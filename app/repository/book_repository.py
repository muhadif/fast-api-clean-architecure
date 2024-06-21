from contextlib import AbstractContextManager
from typing import Callable, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicatedError, InternalError
from app.model.model import Book, Author
from app.schema.book import CreateBook, GetBookRequest, GetBookResponse, Book as BookSchema
from app.schema.author import Author as AuthorSchema



class BookRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.model = Book

    def get(self, req: GetBookRequest):
        with self.session_factory() as session:
            query = session.query(Book)
            if req.author_id != 0:
                query = query.filter(req.author_id == Book.author_id)

            total = query.count()

            booksModel = query.offset((req.page - 1) * req.pageSize).limit(req.pageSize).all()

            bookchema = []
            for book in booksModel:
                author = AuthorSchema(id=book.author.id, name=str(book.author.name), birthdate=str(book.author.birthdate), bio=str(book.author.bio))
                bookchema.append(BookSchema(id=book.id, title=book.title, description=book.description, publish_date=book.publish_date,
                           author_id=book.author_id, author=author))

            resp = GetBookResponse(
                books=bookchema,
                page=req.page,
                pageSize=req.pageSize,
                total=total
            )

            return resp

    def get_by_id(self, id: int) -> Type[Book] | None:
        with self.session_factory() as session:
            return session.query(self.model).filter_by(id=id).first()

    def create(self, book : Book):
        with self.session_factory() as session:
            query = book
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query

    def update(self, book : Book):
        with self.session_factory() as session:
            try:
                session.query(Book).filter(book.id == Book.id).update({
                    'title': book.title,
                    'description': book.description,
                    'author_id': book.author_id,
                    'publish_date': book.publish_date
                })
                session.commit()
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            except Exception as e:
                raise InternalError(detail=str(e))
            return book

    def delete(self, id: int):
        with self.session_factory() as session:
            try:
                session.query(Book).filter(id == Book.id).delete()
                session.commit()
            except Exception as e:
                raise InternalError(detail=str(e))
            pass

    def delete_by_author_id(self, author_id: int):
        with self.session_factory() as session:
            try:
                session.query(Book).filter(author_id == Book.author_id).delete()
                session.commit()
            except Exception as e:
                raise InternalError(detail=str(e))
            pass




