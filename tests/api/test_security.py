"""Api security tests."""

import uuid
from datetime import timedelta

from jose import jwt

from users_api.api import security
from users_api.settings import get_settings

settings = get_settings()


def test_password_hashing():
    """Security password hashing test."""
    plain_password = "some_password"
    hashed_password = security.get_password_hash(plain_password)
    assert security.verify_password(plain_password, hashed_password)


def test_generate_jwt():
    """JWT generation test."""
    uid = uuid.uuid4()
    access_token = security.create_access_token(data=uid)

    decoded_token = jwt.decode(
        access_token,
        settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )

    assert decoded_token["sub"] == str(uid)


def test_generate_jwt_with_different_expire_time():
    """JWT generation with different expire_time test."""
    uid = uuid.uuid4()
    access_token = security.create_access_token(
        data=uid,
        expires_delta=timedelta(minutes=10),
    )

    decoded_token = jwt.decode(
        access_token,
        settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )

    assert decoded_token["sub"] == str(uid)
