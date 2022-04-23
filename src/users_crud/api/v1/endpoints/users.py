"""Endpoints related to Users."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from users_crud import crud, schemas
from users_crud.api import deps
from users_crud.models.user import User

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
    current_user: User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
) -> Any:
    """Retrieve an existing User.

    Args:
        db (Session): A database session
        current_user (User): Logged in User
        user_id (uuid.UUID): The uuid of the user to retrieve

    Raises:
        HTTPException: When a resource with the given id is not found
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
    current_superuser: User = Depends(deps.get_current_superuser),
) -> Any:
    """Retrieve many users.

    Args:
        db (Session): A database session
        current_superuser (User): Currently logged in superuser
    """
    instance_list = crud.user.get_multi(db)
    return instance_list


@router.post(
    "",
    response_model=schemas.UserCreateOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a User",
    description="Create a User",
)
async def create(
    *,
    db: Session = Depends(deps.get_db),
    instance_in: schemas.UserCreateIn,
) -> Any:
    """Create a new user.

    Args:
        db (Session): A database session
        instance_in (schemas.UserCreateIn): Input data
    """
    instance = crud.user.create(db, obj_in=instance_in)
    return instance


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
    current_user: User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
    user_in: schemas.UserUpdateIn,
) -> Any:
    """Update an existing User.

    Args:
        db (Session): A database session
        current_user (User): Logged in Userç
        user_id (uuid.UUID): The uuid of the user to modify
        user_in (schemas.UserUpdateIn): The new data

    Raises:
        HTTPException: When a resource with the given id is not found
    """
    if current_user.uuid == user_id:
        instance_db = current_user
    elif current_user.is_superuser:
        instance_db = crud.user.get_by_uuid(db, uuid=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    if instance_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    updated_instance = crud.user.update(db, db_obj=instance_db, obj_in=user_in)

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
    current_user: User = Depends(deps.get_current_user),
    user_id: uuid.UUID,
    update_password_data: schemas.UserUpdatePasswordIn,
) -> Any:
    """Update an existing User.

    Args:
        db (Session): A database session
        current_user (User): Logged in User
        user_id (uuid.UUID): The uuid of the user to modify
        update_password_data (schemas.UserUpdatePasswordIn): The update password data

    Raises:
        HTTPException: When a resource with the given id is not found, the user
            does not have enough privileges or the submitted password is incorrect
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
