"""JWT Generation and password hashing."""

from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from users_api.settings import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: str | Any, expires_delta: timedelta = None) -> str:
    """Create access token.

    Args:
        data (str | Any): Data to be encoded in token
        expires_delta (timedelta): Access token expire time

    Returns:
        str: The generated access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(data)}
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plain_password vs hashed_password using pwd_context.

    Args:
        plain_password (str): Password in plain text
        hashed_password (str): Previously hashed password

    Returns:
        bool: Whether the password was successfully verified or not
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Return a hashed password using pwd_context.

    Args:
        password (str): Password in plain text

    Returns:
        str: Hashed password using pwd_context
    """
    return pwd_context.hash(password)
