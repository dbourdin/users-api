"""User Schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from users_crud.schemas import APIMessage, APISchema


class BaseUserSchema(APISchema):
    """Base User API Model."""

    first_name: str | None = Field(example="John")
    last_name: str | None = Field(example="Doe")


class BaseUserSchemaWithUsername(BaseUserSchema):
    """Base User API Model with username."""

    username: str = Field(..., example="my_username")


class UserCreateIn(BaseUserSchemaWithUsername):
    """Parameters received in a POST request."""

    password: str = Field(..., example="my_password")
    is_superuser: bool = False


class UserCreateDB(UserCreateIn):
    """Model used to create a new record in a POST request."""


class UserCreateOut(BaseUserSchemaWithUsername):
    """Parameters returned in a POST request."""

    uuid: UUID
    created_at: datetime
    updated_at: datetime


class UserGet(UserCreateOut):
    """Parameters returned in a GET request."""


class UserList(UserGet):
    """Parameters returned in a GET LIST request."""


class UserUpdateIn(BaseUserSchema):
    """Parameters received in a PUT request."""


class UserUpdateDB(UserUpdateIn):
    """Model used to update a record in a PUT request."""


class UserUpdateOut(UserCreateOut):
    """Parameters returned in a PUT request."""


class UserUpdatePasswordIn(APISchema):
    """Parameters received in an update password PUT request."""

    old_password: str = Field("", example="my_old_password")
    new_password: str = Field(..., example="my_new_password")


class UserUpdatePasswordDB(UserUpdatePasswordIn):
    """Model used to update a User password in an update password PUT request."""


class UserUpdatePasswordOut(APIMessage):
    """Parameters returned in an update password PUT request."""
