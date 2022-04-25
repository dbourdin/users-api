"""User database table."""

from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.declarative import declared_attr

from users_api.api import security
from users_api.db.base_class import Base


class User(Base):
    """User database table."""

    username = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String)
    is_superuser = Column(Boolean(), default=False)

    @property
    def password(self):
        """Block password from being read."""
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        """Password hashing."""
        self.password_hash = security.get_password_hash(password)

    def verify_password(self, password):
        """Password validator."""
        return security.verify_password(password, self.password_hash)

    @declared_attr
    def __tablename__(cls) -> str:
        """Return the table name."""
        return "users"
