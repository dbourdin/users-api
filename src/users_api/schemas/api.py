"""API Version information."""

from users_api.schemas.base import APISchema


class ApiVersionModel(APISchema):
    """Data structure to hold the API version information."""

    title: str
    description: str
    version: str
