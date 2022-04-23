"""CRUD for Users."""

from sqlalchemy.orm import Session

from users_crud.crud.base import CRUDBase
from users_crud.models.user import User
from users_crud.schemas import UserCreateDB, UserUpdateDB


class CRUDUser(CRUDBase[User, UserCreateDB, UserUpdateDB]):
    """CRUD for Users."""

    @staticmethod
    def _get_by_username(db: Session, *, username: str) -> User | None:
        """Get User by username.

        Args:
            db (Session): A database session
            username (str): Username to be looked up

        Returns:
            User: The retrieved User
        """
        return db.query(User).filter(User.username == username).first()

    def authenticate(self, db: Session, *, username: str, password: str) -> User | None:
        """Authenticate by username and password.

        Args:
            db (Session): A database session
            username (str): Username to be authenticated
            password(str): Password used to authenticate

        Returns:
            User: The authenticated User
        """
        user_ = self._get_by_username(db, username=username)
        if not user_:
            return None
        if not user_.verify_password(password):
            return None
        return user_

    @staticmethod
    def update_password(
        db: Session,
        *,
        db_user: User,
        new_password: str,
    ) -> User:
        """Update a row.

        Args:
            db (Session): A database session
            db_user (User): Old user in db
            new_password (str): New password to be updated

        Returns:
            User: The updated User
        """
        if new_password:
            db_user.password = new_password
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user = CRUDUser(User)
