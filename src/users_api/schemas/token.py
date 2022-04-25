"""Token Schemas."""
from pydantic import BaseModel

from users_api.schemas import APISchema


class Token(BaseModel):
    """Token Schema."""

    access_token: str
    token_type: str


class TokenData(APISchema):
    """TokenData Schema."""

    exp: str
    sub: str
