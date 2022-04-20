#!/usr/local/bin/python

"""Main API CLI file."""

from pprint import pformat

import typer
import uvicorn

from users_crud.settings import get_settings

app = typer.Typer()
settings = get_settings()


@app.command()
def start_reload():
    """Start the API with Uvicorn in reload mode."""
    uvicorn_settings = settings.get_uvicorn_settings()
    print(f"Starting uvicorn with these settings: \n{pformat(uvicorn_settings)}")
    uvicorn.run(**uvicorn_settings)


if __name__ == "__main__":
    app()
