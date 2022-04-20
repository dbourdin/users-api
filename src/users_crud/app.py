"""API initialization and setup file."""

from fastapi import FastAPI

from users_crud.api.v1.routers import router
from users_crud.schemas import ApiVersionModel
from users_crud.settings import EnvironmentEnum, Settings, get_settings

settings = get_settings()

app = FastAPI(
    title="Users CRUD API",
    description="Users CRUD API",
    version=settings.API_VERSION,
    debug=settings.ENVIRONMENT == EnvironmentEnum.development,
    root_path=settings.ROOT_PATH,
)
app.include_router(router, prefix="/v1")


@app.get("/version", tags=["version"], response_model=ApiVersionModel)
def get_api_version():
    """Get API information."""
    return ApiVersionModel(
        title=app.title, description=app.description, version=app.version
    )


if settings.ENVIRONMENT == EnvironmentEnum.development:

    @app.get("/settings", tags=["settings"], response_model=Settings)
    def get_api_settings():
        """Get API Settings."""
        return settings
