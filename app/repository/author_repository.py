from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, Type

from cacheout import Cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.cacbe import CacheMemory
from app.core.exceptions import DuplicatedError, InternalError
from app.model.model import Author
from app.schema.author import CreateAuthor, GetAuthorRequest, GetAuthorResponse, Author as AuthorSchema


class AuthorRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]],
                 cache: CacheMemory) -> None:
        self.session_factory = session_factory
        self.model = Author
        self.cache = cache

    def get(self, req: GetAuthorRequest):
        with self.session_factory() as session:
            try:
                query = session.query(Author)
                if req.name != "":
                    query = query.filter(req.name == Author.name)

                total = query.count()

                authorsModel = query.offset((req.page - 1) * req.pageSize).limit(req.pageSize).all()

                authorsSchema = [AuthorSchema(id=author.id, name=str(author.name), birthdate=str(author.birthdate),
                                              bio=str(author.bio)) for author in authorsModel]

                resp = GetAuthorResponse(
                    authors=authorsSchema,
                    page=req.page,
                    pageSize=req.pageSize,
                    total=total
                )
            except Exception as e:
                print(e)
                raise InternalError(detail=str(e))
            return resp

    def get_by_id(self, id: int) -> Type[Author] | None:
        cache_key = f"author_get_by_id_{id}"
        with self.session_factory() as session:
            try:
                author = self.cache.get(cache_key)
                if author is None:
                    author = session.query(self.model).filter_by(id=id).first()
                    self.cache.set(cache_key, author)
            except Exception as e:
                raise InternalError(e)
            return author


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



