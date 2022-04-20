"""User database table."""

import bcrypt
from sqlalchemy import Column, String

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
        salt = bcrypt.gensalt()
        if isinstance(password, str):
            password = password.encode("utf8")
        self.password_hash = bcrypt.hashpw(password, salt)

    def verify_password(self, password):
        """Password validator."""
        if isinstance(password, str):
            password = password.encode("utf8")
        return bcrypt.checkpw(password, self.password_hash)
