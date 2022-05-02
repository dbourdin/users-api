"""API FastAPI dependencies."""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from users_api import crud, schemas
from users_api.db.session import SessionLocal
from users_api.models.user import User
from users_api.settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


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


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get current User based on JWT Bearer.

    Args:
        db (Session): A database session
        token (str): The JWT Bearer

    Raises:
        HTTPException: When a resource with the given id is not found,
            or invalid credentials were provided

    Returns:
        User: Current User
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get_by_uuid(db, uuid=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Get current superuser based on JWT Bearer.

    Args:
        current_user (User): Current User based on JWT Bearer.

    Raises:
        HTTPException: When a resource with the given id is not found,
            or invalid credentials for superuser were provided

    Returns:
        User: Current superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return current_user
