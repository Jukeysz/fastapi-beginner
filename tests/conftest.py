import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture()
def client(session):
    # we are stablishing that the get_session dependency will come
    # from the memory db for the tests, as stated in the row 19
    # and not from the real session
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client


@pytest.fixture()
def user(session):
    user = User(username='test', email='test@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def session():
    # mem database is faster than disk db for unit testing
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
