"""Testing utils."""

import typing
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI


class DependencyOverrider:
    """DependencyOverrider for testing purposes."""

    def __init__(
        self, app: FastAPI, overrides: typing.Mapping[typing.Callable, typing.Callable]
    ) -> None:
        """Initialize DependencyOverrider."""
        self.overrides = overrides
        self._app = app
        self._old_overrides = {}

    def __enter__(self):
        """Add overrides."""
        for dep, new_dep in self.overrides.items():
            if dep in self._app.dependency_overrides:
                # Save existing overrides
                self._old_overrides[dep] = self._app.dependency_overrides[dep]
            self._app.dependency_overrides[dep] = new_dep
        return self

    def __exit__(self, *args: typing.Any) -> None:
        """Restore previous overrides."""
        for dep in self.overrides.keys():
            if dep in self._old_overrides:
                # Restore previous overrides
                self._app.dependency_overrides[dep] = self._old_overrides.pop(dep)
            else:
                # Just delete the entry
                del self._app.dependency_overrides[dep]


dt = datetime.now(timezone.utc)
TEST_USER = {
    "uuid": uuid.uuid4(),
    "username": "test_username",
    "password": "password",
    "created_at": dt,
    "updated_at": dt,
}

TEST_SUPERUSER = TEST_USER.copy()
TEST_SUPERUSER["uuid"] = uuid.uuid4()
TEST_SUPERUSER["username"] = "admin"
TEST_SUPERUSER["password"] = "admin"
TEST_SUPERUSER["is_superuser"] = True
