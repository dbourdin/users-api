"""Token Schemas."""

from users_crud.schemas.base import APISchema


class Token(APISchema):
    """Token Schema."""

    access_token: str
    token_type: str


class TokenData(APISchema):
    """TokenData Schema."""

    uuid: str | None = None
