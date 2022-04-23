"""Endpoints related to Users."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from users_crud import crud, schemas
from users_crud.api import deps

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=schemas.UserGet,
    responses={status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage}},
    summary="Retrieve a single User by UUID",
    description="Retrieve single a User by UUID",
)
async def get(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
) -> Any:
    """Retrieve an existing User.

    Args:
        user_id (uuid.UUID): The uuid of the user to retrieve
        db (Session): A database session

    Raises:
        HTTPException: When a resource with the given id is not found
    """
    instance_db = crud.user.get_by_uuid(db, uuid=user_id)
    if instance_db is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with Id {user_id} was not found",
        )

    return instance_db


@router.get(
    "",
    response_model=list[schemas.UserList],
    summary="List Users",
    description="Get a list of Users",
)
def retrieve_many(
    db: Session = Depends(deps.get_db),
) -> Any:
    """Retrieve many users.

    Args:
        db (Session): A database session
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
        instance_in (schemas.UserCreateIn): Input data
        db (Session): A database session
    """
    instance = crud.user.create(db, obj_in=instance_in)
    return instance


@router.put(
    "/{user_id}",
    response_model=schemas.UserUpdateOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": schemas.APIMessage}},
    summary="Edit a User",
    description="Edit a User",
)
async def update(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    user_in: schemas.UserUpdateIn,
) -> Any:
    """Update an existing User.

    Args:
        user_id (uuid.UUID): The uuid of the user to modify
        user_in (schemas.UserUpdateIn): The new data
        db (Session): A database session

    Raises:
        HTTPException: When a resource with the given id is not found
    """
    instance_db = crud.user.get_by_uuid(db, uuid=user_id)
    if instance_db is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with Id {user_id} was not found",
        )
    updated_instance = crud.user.update(db, db_obj=instance_db, obj_in=user_in)

    return updated_instance
