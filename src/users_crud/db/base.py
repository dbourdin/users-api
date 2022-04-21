# Import all the models, so that Base has them before being
# imported by Alembic
# flake8: noqa

from users_crud.db.base_class import Base
from users_crud.models.user import User
