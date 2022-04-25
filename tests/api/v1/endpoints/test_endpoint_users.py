"""Test /users endpoints."""

import uuid
from datetime import datetime, timezone
from unittest import mock

from fastapi import status
from fastapi.testclient import TestClient

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
