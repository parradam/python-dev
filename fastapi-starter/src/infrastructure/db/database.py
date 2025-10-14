from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import get_settings

settings = get_settings()

sqlite_url = f"sqlite:///{settings.sqlite_path}"

engine = create_engine(sqlite_url, echo=(settings.ENV != "prod"))

SessionDep = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Generator[Session]:
    session = SessionDep()
    try:
        yield session
    finally:
        session.close()



