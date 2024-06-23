import datetime
import os
import unittest

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util.preloaded import orm
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from app.core.config import configs
from app.main import AppCreator
from app.model.model import Base, Author, Book

os.environ["ENV"] = "test"

if os.getenv("ENV") not in ["test"]:
    msg = f"ENV is not test, it is {os.getenv('ENV')}"
    pytest.exit(msg)


def seeding(session):
    try:
        session.add(Author(name="adif", bio="hi", birthdate=datetime.datetime.fromisoformat("2024-06-20")))
        session.add(Author(name="adif-2", bio="hello", birthdate=datetime.datetime.fromisoformat("2023-06-20")))
        session.add(Book(title="Diary", description="Diary adif", publish_date=datetime.datetime.fromisoformat("2023-06-20"), author_id=2))
        session.add(Book(title="Journal", description="Journal adif", publish_date=datetime.datetime.fromisoformat("2023-06-20"), author_id=1))
        session.commit()
    except Exception as e:
        print("error",e)


def reset_db():
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            ),
        )

    seeding(session)
    return engine


@pytest.fixture
def client():
    reset_db()

    app_creator = AppCreator()
    app = app_creator.app

    with TestClient(app) as client:
        yield client


