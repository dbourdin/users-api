"""Endpoints related to Users."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from users_api import crud, models, schemas
from users_api.api import deps

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=schemas.UserGet,
    responses={
        status.HTTP_403_FORBIDDEN: {"model": schemas.APIMessage},
        status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage},
    },
    summary="Retrieve a single User by UUID",
    description="Retrieve single a User by UUID",
)
async def get(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
) -> Any:
    """Retrieve an existing User.

    Args:
        db (Session): A database session
        current_user (models.User): Logged in User
        user_id (uuid.UUID): The uuid of the user to retrieve

    Raises:
        HTTPException: List of exceptions:
            - HTTP_403_FORBIDDEN: If the user doesn't have enough privileges.
            - HTTP_404_NOT_FOUND: If the user does not exist.
    """
    if current_user.uuid == user_id:
        return current_user

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    db_user = crud.user.get_by_uuid(db, uuid=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return db_user


@router.get(
    "",
    response_model=list[schemas.UserList],
    summary="List Users",
    description="Get a list of Users",
)
def retrieve_many(
    db: Session = Depends(deps.get_db),
    current_superuser: models.User = Depends(deps.get_current_superuser),
) -> Any:
    """Retrieve many users.

    Args:
        db (Session): A database session
        current_superuser (models.User): Currently logged in superuser
    """
    instance_list = crud.user.get_multi(db)
    return instance_list


@router.post(
    "",
    response_model=schemas.UserCreateOut,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"model": schemas.APIMessage}},
    summary="Create a User",
    description="Create a User",
)
async def create(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateIn,
) -> Any:
    """Create a new user.

    Args:
        db (Session): A database session
        user_in (schemas.UserCreateIn): Input data

    Raises:
        HTTPException: List of exceptions:
            - HTTP_400_BAD_REQUEST: If username already exists.
    """
    try:
        db_user = crud.user.create(db, obj_in=user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{user_in.username}' already exists",
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=schemas.UserUpdateOut,
    responses={
        status.HTTP_403_FORBIDDEN: {"model": schemas.APIMessage},
        status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage},
    },
    summary="Edit a User",
    description="Edit a User",
)
async def update(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
    user_in: schemas.UserUpdateIn,
) -> Any:
    """Update an existing User.

    Args:
        db (Session): A database session
        current_user (models.User): Logged in User
        user_id (uuid.UUID): The uuid of the user to modify
        user_in (schemas.UserUpdateIn): The new data

    Raises:
        HTTPException: List of exceptions:
            - HTTP_403_FORBIDDEN: If the user doesn't have enough privileges.
            - HTTP_404_NOT_FOUND: If the user does not exist.
    """
    if current_user.uuid == user_id:
        db_user = current_user
    elif current_user.is_superuser:
        db_user = crud.user.get_by_uuid(db, uuid=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    updated_instance = crud.user.update(db, db_obj=db_user, obj_in=user_in)

    return updated_instance


@router.put(
    "/{user_id}/password",
    response_model=schemas.UserUpdatePasswordOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": schemas.APIMessage},
        status.HTTP_403_FORBIDDEN: {"model": schemas.APIMessage},
        status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage},
    },
    summary="Edit a User",
    description="Edit a User",
)
async def update_password(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
    update_password_data: schemas.UserUpdatePasswordIn,
) -> Any:
    """Update an existing User.

    Args:
        db (Session): A database session
        current_user (models.User): Logged in User
        user_id (uuid.UUID): The uuid of the user to modify
        update_password_data (schemas.UserUpdatePasswordIn): The update password data

    Raises:
        HTTPException: List of exceptions:
            - HTTP_400_BAD_REQUEST: If old_password is incorrect.
            - HTTP_403_FORBIDDEN: If the user doesn't have enough privileges.
            - HTTP_404_NOT_FOUND: If the user does not exist.
    """
    if current_user.uuid == user_id:
        db_user = current_user
    elif current_user.is_superuser:
        db_user = crud.user.get_by_uuid(db, uuid=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not current_user.is_superuser and not db_user.verify_password(
        update_password_data.old_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submitted password does not match",
        )

    crud.user.update_password(
        db, db_user=db_user, new_password=update_password_data.new_password
    )

    return schemas.UserUpdatePasswordOut(detail="Password updated successfully")


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": schemas.APIMessage},
        status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage},
    },
    summary="Delete a User",
    description="Delete a User",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
) -> Any:
    """Update an existing User.

    Args:
        db (Session): A database session
        current_user (models.User): Logged in User
        user_id (uuid.UUID): The uuid of the user to modify

    Raises:
        HTTPException: List of exceptions:
            - HTTP_403_FORBIDDEN: If the user doesn't have enough privileges.
            - HTTP_404_NOT_FOUND: If provided user_id doesn't exist.
    """
    if current_user.uuid == user_id:
        db_user = current_user
    elif current_user.is_superuser:
        db_user = crud.user.get_by_uuid(db, uuid=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    crud.user.remove(db, id=db_user.id)
