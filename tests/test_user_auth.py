import pytest
from db.user_auth import add_user, authenticate_user

def test_add_and_authenticate_user(tmp_path, monkeypatch):
    # Patch database URL to use a temporary database
    from db import database
    database.DATABASE_URL = f"sqlite:///{tmp_path}/test.db"
    database.engine = database.create_engine(database.DATABASE_URL)
    database.Session = database.sessionmaker(bind=database.engine)
    database.Base.metadata.create_all(database.engine)

    # Create user
    username = "test_user"
    password = "test_password"
    add_user(username, password, role="user")

    # Authenticate
    user = authenticate_user(username, password)
    assert user is not None
    assert user.username == username

    # Wrong password
    assert authenticate_user(username, "wrong") is None