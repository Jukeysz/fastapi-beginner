import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    # mem database is faster than disk db for unit testing
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    '''
        Considerations: each time I make a test with this fixture,
        I am gonna make a session, connect to an engine and create
        the metadata which are translated to columns.
        The key part is the generator function that throws
        sessions each time the fixture is called.
    '''
    table_registry.metadata.drop_all(engine)
