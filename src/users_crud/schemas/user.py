"""User Schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from users_crud.schemas.base import APISchema


class BaseUserSchema(APISchema):
    """Base User API Model."""

    username: str = Field(..., example="my_username")
    first_name: str | None = Field(example="John")
    last_name: str | None = Field(example="Doe")


class UserCreateIn(BaseUserSchema):
    """Parameters received in a POST request."""

    password: str = Field(..., example="my_password")


class UserCreateDB(UserCreateIn):
    """Model used to create a new record in a POST request."""


class UserCreateOut(BaseUserSchema):
    """Parameters returned in a POST request."""

    uuid: UUID
    username: str
    first_name: str | None
    last_name: str | None
    created_at: datetime
    updated_at: datetime


class UserList(UserCreateOut):
    """Parameters returned in a GET LIST request."""


class UserUpdateIn(UserCreateIn):
    """Parameters received in a PUT request."""


class UserUpdateDB(UserCreateDB):
    """Model used to update a record in a PUT request."""


class UserUpdateOut(UserCreateOut):
    """Parameters returned in a PUT request."""
