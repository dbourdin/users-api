"""User database table."""

from sqlalchemy import Column, String

from users_crud.db.base_class import Base


class User(Base):
    """User database table."""

    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
