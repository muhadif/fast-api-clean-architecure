from dependency_injector import containers, providers

from app.core.cacbe import CacheMemory
from app.core.database import Database
from app.core.config import configs
from app.repository.author_repository import AuthorRepository
from app.repository.book_repository import BookRepository
from app.service.author_service import AuthorService
from app.service.book_service import BookService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.author",
            "app.api.endpoints.book",
        ]
    )

    db = providers.Singleton(Database, db_url= configs.DATABASE_URI)
    cache = providers.Singleton(CacheMemory)

    author_repository = providers.Factory(AuthorRepository, session_factory=db.provided.session, cache=cache)
    book_repository = providers.Factory(BookRepository, session_factory=db.provided.session, cache=cache)

    author_service = providers.Factory(AuthorService, author_repository=author_repository, book_repository=book_repository)
    book_service = providers.Factory(BookService, book_repository=book_repository)
