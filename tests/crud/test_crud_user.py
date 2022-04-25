"""Test the crud class of Users."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from users_api import crud, schemas


def test_list_users_empty(
    db_fixture: Session,
):
    """Can list Users when none is created."""
    users = crud.user.get_multi(db_fixture)
    assert users == []


def test_create_user(
    db_fixture: Session,
    create_user_data,
):
    """Can create a new User."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    assert created_user.username == create_user_data["username"]


def test_update_user(
    db_fixture: Session,
    create_user_data,
):
    """Can update a created User."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    update_user_data = {
        "first_name": "John",
        "last_name": "Doe",
    }

    updated_user = crud.user.update(
        db_fixture,
        obj_in=update_user_data,
        db_obj=created_user,
    )
    assert updated_user.first_name == update_user_data["first_name"]
    assert updated_user.last_name == update_user_data["last_name"]


def test_update_user_from_schema(
    db_fixture: Session,
    create_user_data,
):
    """Can update a created User."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    update_user_data = {
        "first_name": "John",
        "last_name": "Doe",
    }
    update_user_schema = schemas.user.UserUpdateIn(**update_user_data)

    updated_user = crud.user.update(
        db_fixture,
        obj_in=update_user_schema,
        db_obj=created_user,
    )
    assert updated_user.first_name == update_user_schema.first_name
    assert updated_user.last_name == update_user_schema.last_name


def test_user_created_at(
    db_fixture: Session,
    create_user_data,
):
    """The `created_at` field is filled automatically when a row is created."""
    now_before = datetime.now(timezone.utc)

    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    now_after = datetime.now(timezone.utc)

    assert now_before < created_user.created_at < now_after


def test_user_many_created_at(
    db_fixture: Session,
    create_user_data_multi,
):
    """The `created_at` field is filled automatically when a row is created."""
    user_1 = crud.user.create(db=db_fixture, obj_in=create_user_data_multi[0])
    user_2 = crud.user.create(db=db_fixture, obj_in=create_user_data_multi[1])

    assert user_1.created_at < user_2.created_at


def test_user_updated_at(
    db_fixture: Session,
    create_user_data,
):
    """The `updated_at` field is rewritten on a row update."""
    update_user_data = {
        "first_name": "John",
        "last_name": "Doe",
    }

    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    old_updated_at = created_user.updated_at

    updated_user = crud.user.update(
        db=db_fixture,
        db_obj=created_user,
        obj_in=update_user_data,
    )

    assert old_updated_at < updated_user.updated_at


def test_list_users(
    db_fixture: Session,
    create_user_data_multi,
):
    """Retrieve a list of users."""
    user_1 = crud.user.create(db=db_fixture, obj_in=create_user_data_multi[0])
    user_2 = crud.user.create(db=db_fixture, obj_in=create_user_data_multi[1])

    items = crud.user.get_multi(db=db_fixture)

    assert len(items) == len(create_user_data_multi)
    assert user_1 in items
    assert user_2 in items


def test_get_user_by_id(
    db_fixture: Session,
    create_user_data,
):
    """Retrieve a user by id."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    retrieved_user = crud.user.get(db_fixture, id=created_user.id)

    assert retrieved_user == created_user


def test_get_user_by_uuid(
    db_fixture: Session,
    create_user_data,
):
    """Retrieve a user by uuid."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    retrieved_user = crud.user.get_by_uuid(db_fixture, uuid=created_user.uuid)

    assert retrieved_user == created_user


def test_remove_user(
    db_fixture: Session,
    create_user_data,
):
    """Can remove a user."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    _ = crud.user.remove(db_fixture, id=created_user.id)

    items = crud.user.get_multi(db=db_fixture)

    assert len(items) == 0


def test_get_user_by_username(
    db_fixture: Session,
    create_user_data,
):
    """Retrieve a user by username."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    retrieved_user = crud.user._get_by_username(
        db_fixture,
        username=created_user.username,
    )

    assert retrieved_user == created_user


def test_authenticate_user(
    db_fixture: Session,
    create_user_data,
):
    """Authenticate username by username and password."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)

    auth_user = crud.user.authenticate(
        db_fixture,
        username=create_user_data["username"],
        password=create_user_data["password"],
    )

    assert auth_user == created_user


def test_authenticate_user_with_invalid_username_returns_none(
    db_fixture: Session,
    create_user_data,
):
    """Authenticate user with invalid username."""
    _ = crud.user.create(db_fixture, obj_in=create_user_data)

    auth_user = crud.user.authenticate(
        db_fixture,
        username="invalid_username",
        password=create_user_data["password"],
    )

    assert not auth_user


def test_authenticate_user_with_invalid_password_returns_none(
    db_fixture: Session,
    create_user_data,
):
    """Authenticate user with invalid password."""
    _ = crud.user.create(db_fixture, obj_in=create_user_data)

    auth_user = crud.user.authenticate(
        db_fixture,
        username=create_user_data["username"],
        password="invalid_password",
    )

    assert not auth_user


def test_update_user_password(
    db_fixture: Session,
    create_user_data,
):
    """Update user password."""
    created_user = crud.user.create(db_fixture, obj_in=create_user_data)
    new_password = "new_password"
    updated_user = crud.user.update_password(
        db_fixture,
        db_user=created_user,
        new_password=new_password,
    )

    assert updated_user.verify_password(new_password)
