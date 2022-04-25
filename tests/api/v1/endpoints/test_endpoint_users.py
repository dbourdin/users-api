"""Test /users endpoints."""

import uuid
from datetime import datetime, timezone
from unittest import mock

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from tests.conftest import TEST_USER
from users_api import schemas


@mock.patch("users_api.api.v1.endpoints.users.crud.user")
def test_create_user(
    crud_user_mock,
    client: TestClient,
):
    """Create a User via POST."""
    user = {"username": "test_user", "password": "password"}
    data_to_send = schemas.UserCreateIn(**user)

    uid = uuid.uuid4()
    dt = datetime.now(timezone.utc)
    return_value = {
        "username": user["username"],
        "uuid": uid,
        "created_at": dt,
        "updated_at": dt,
    }
    crud_user_mock.create.return_value = return_value

    response = client.post("/v1/users", json=data_to_send.dict())

    assert response.status_code == status.HTTP_201_CREATED, response.text

    received = schemas.UserCreateOut.parse_raw(response.text)
    expected = schemas.UserCreateOut.parse_obj(return_value)
    assert received == expected

    crud_user_mock.create.assert_called_once()


@mock.patch("users_api.api.v1.endpoints.users.crud.user")
def test_create_user_integrity_error_throws_400(
    crud_user_mock,
    client: TestClient,
):
    """Create a User via POST."""
    user = {"username": "test_user", "password": "password"}
    data_to_send = schemas.UserCreateIn(**user)
    crud_user_mock.create.side_effect = IntegrityError(
        "IntegrityError", "params", "orig"
    )

    response = client.post("/v1/users", json=data_to_send.dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    crud_user_mock.create.assert_called_once()


def test_get_user(
    client: TestClient,
    # override get_current_user to return TEST_USER
    mock_current_user,
):
    """Get a User via GET."""
    response = client.get(f"/v1/users/{TEST_USER['uuid']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    received = schemas.UserGet.parse_raw(response.text)
    expected = schemas.UserGet.parse_obj(TEST_USER)
    assert received == expected


def test_get_user_throws_401_if_unauthorized(
    client: TestClient,
):
    """Get User returns 401 if unauthorized."""
    uid = uuid.uuid4()
    response = client.get(f"/v1/users/{uid}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_get_user_without_privileges_throws_403(
    client: TestClient,
    # override get_current_user to return TEST_USER
    mock_current_user,
):
    """Get User returns 403 if unauthorized."""
    response = client.get(f"/v1/users/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text


@mock.patch("users_api.api.v1.endpoints.users.crud.user")
def test_get_user_as_superuser(
    crud_user_mock,
    client: TestClient,
    # override get_current_user to return superuser
    mock_current_user_superuser,
):
    """Get User returns as superuser."""
    crud_user_mock.get_by_uuid.return_value = TEST_USER
    response = client.get(f"/v1/users/{TEST_USER['uuid']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    received = schemas.UserGet.parse_raw(response.text)
    expected = schemas.UserGet.parse_obj(TEST_USER)
    assert received == expected
