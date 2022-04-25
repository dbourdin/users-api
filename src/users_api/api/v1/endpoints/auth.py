"""Endpoints related to Authentication."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from users_api import crud, schemas
from users_api.api import deps
from users_api.api.security import create_access_token
from users_api.models.user import User

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Login",
    description="Login",
)
async def login_for_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.Token:
    """Retrieve an existing User.

    Args:
        db (Session): A database session
        form_data (OAuth2PasswordRequestForm): form data containing User credentials

    Raises:
        HTTPException: If the User cannot be authenticated
    """
    user: User = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=user.uuid, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
