"""API Settings."""

from enum import Enum
from functools import lru_cache
from ipaddress import IPv4Address
from typing import Any

from pydantic import BaseSettings, PositiveInt, PostgresDsn, validator

from users_crud.version import __version__


class EnvironmentEnum(str, Enum):
    """API Environment Enum."""

    production = "production"
    development = "development"


class LoggingEnum(str, Enum):
    """Logging configuration Enum."""

    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class APISettings(BaseSettings):
    """Basic API settings.

    Includes database configuration, environment, CORS and logging, among others.
    """

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.production

    API_VERSION: str = __version__

    LOGLEVEL: LoggingEnum = LoggingEnum.info

    # Settings related to running an ASGI app
    APP_MODULE: str = "users_crud.app:app"
    HOST: IPv4Address = "0.0.0.0"
    PORT: PositiveInt = 3000

    def get_uvicorn_settings(self) -> dict[str, Any]:
        """Get a dictionary with settings ready to be used by Uvicorn."""
        return {
            "app": self.APP_MODULE,
            "host": str(self.HOST),
            "port": self.PORT,
            "log_level": self.LOGLEVEL.lower(),  # Uvicorn expects lowercase strings
            "reload": True,
        }

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    POSTGRES_TEST_DB: str | None = "test.users_crud"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        """Assemble the database connection URL."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    # To use the API behind a proxy, set this variable to the desired base route
    # This will make the /docs URL work properly
    # More info here: https://fastapi.tiangolo.com/advanced/behind-a-proxy/
    ROOT_PATH: str = ""


class Settings(APISettings):
    """API settings.

    Includes configuration tied specifically to this API.
    """


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the API Settings."""
    return Settings()
