from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicatedError, InternalError
from app.model.model import Author
from app.schema.author import CreateAuthor, GetAuthorRequest, GetAuthorResponse, Author as AuthorSchema


class AuthorRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.model = Author

    def get(self, req: GetAuthorRequest):
        with self.session_factory() as session:
            query = session.query(Author)
            if req.name != "":
                query = query.filter(req.name == Author.name)

            total = query.count()

            authorsModel = query.offset((req.page - 1) * req.pageSize).limit(req.pageSize).all()

            authorsSchema = [AuthorSchema(id=author.id, name=str(author.name), birthdate=str(author.birthdate), bio=str(author.bio)) for author in authorsModel]

            resp = GetAuthorResponse(
                authors=authorsSchema,
                page=req.page,
                pageSize=req.pageSize,
                total=total
            )

            return resp

    def get_by_id(self, id: int) -> Type[Author] | None:
        with self.session_factory() as session:
            return session.query(self.model).filter_by(id=id).first()

    def create(self, author : Author):
        with self.session_factory() as session:
            query = author
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query

    def update(self, author : Author):
        with self.session_factory() as session:
            try:
                session.query(Author).filter(author.id == Author.id).update({
                    'name': author.name,
                    'bio': author.bio,
                    'birthdate': author.birthdate
                })
                session.commit()
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            except Exception as e:
                raise InternalError(detail=str(e))
            return author

    def delete(self, id: int):
        with self.session_factory() as session:
            try:
                session.query(Author).filter(id == Author.id).delete()
                session.commit()
            except Exception as e:
                raise InternalError(detail=str(e))
            pass



