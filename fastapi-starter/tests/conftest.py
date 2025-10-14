from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.db.database import get_session
from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.resource import Resource  # pyright: ignore[reportUnusedImport] # noqa: F401
from src.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# SQLAlchemy session factory for tests
TestSessionDep = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture(name="session", autouse=True)
def session_fixture() -> Generator[Session]:
    """
    Marks test needing direct database session access (session_fixture).
    """
    # SQLAlchemy metadata can be used for table creation as this is an in-memory DB
    Base.metadata.create_all(bind=test_engine)
    with TestSessionDep() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient]:
    """
    Marks test needing API client with overridden DB session (client_fixture).
    """

    def override_get_session() -> Generator[Session]:
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
