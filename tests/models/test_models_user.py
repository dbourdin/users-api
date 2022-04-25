"""Test the model class of Users."""
import pytest

from users_api import models


def test_cannot_retrieve_user_password_from_model(
    create_user_data,
):
    """Cannot retrieve User password from model."""
    user = models.User(**create_user_data)

    with pytest.raises(AttributeError):
        _ = user.password
