"""User database table."""

from sqlalchemy import Column, String

from users_crud.api import security
from users_crud.db.base_class import Base


class User(Base):
    """User database table."""

    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String)

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
