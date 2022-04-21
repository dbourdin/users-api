"""API FastAPI dependencies."""

from typing import Generator

from users_crud.db.session import SessionLocal


def get_db() -> Generator:
    """Get a db Session.

    Yields:
        Generator: A db Session as a generator
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
