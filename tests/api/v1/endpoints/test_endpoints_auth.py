"""Test /auth endpoints."""

from unittest import mock

from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import TEST_USER
from users_api import models


@mock.patch("users_api.api.v1.endpoints.users.crud.user")
def test_auth(
    crud_user_mock,
    client: TestClient,
):
    """Authenticate using /auth/login."""
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
    }

    crud_user_mock.authenticate.return_value = models.User(**TEST_USER)

    response = client.post("/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK, response.text

    crud_user_mock.authenticate.assert_called_once_with(
        mock.ANY,
        username=login_data["username"],
        password=login_data["password"],
    )


@mock.patch("users_api.api.v1.endpoints.users.crud.user")
def test_auth_with_invalid_credentials_throws_401(
    crud_user_mock,
    client: TestClient,
):
    """Authenticate using /auth/login throws 401 if failed to authenticate."""
    login_data = {
        "username": "some_username",
        "password": "some_password",
    }

    crud_user_mock.authenticate.return_value = None

    response = client.post("/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

    crud_user_mock.authenticate.assert_called_once_with(
        mock.ANY,
        username=login_data["username"],
        password=login_data["password"],
    )
