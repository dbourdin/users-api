"""CRUD for Users."""

from users_crud.crud.base import CRUDBase
from users_crud.models.user import User
from users_crud.schemas import UserCreateDB, UserUpdateDB


class CRUDUser(CRUDBase[User, UserCreateDB, UserUpdateDB]):
    """CRUD for Users."""


user = CRUDUser(User)
