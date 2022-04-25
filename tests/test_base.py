"""Sanity check tests."""

from fastapi import status
from fastapi.testclient import TestClient


def test_import(client: TestClient):
    """Basic FastAPI test."""
    response = client.get("/version")

    assert response.status_code == status.HTTP_200_OK
    assert "Users API" in response.json()["title"]
