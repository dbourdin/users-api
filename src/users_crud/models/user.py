"""User database table."""

from passlib.context import CryptContext
from sqlalchemy import Column, String

from users_crud.db.base_class import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Password validator."""
        return pwd_context.verify(password, self.password_hash)
