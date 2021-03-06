import pytest

from .helpers import add_admin_user_to_database, add_user_roles_to_database


@pytest.fixture(autouse=True)
def clear_database():
    add_user_roles_to_database()
    add_admin_user_to_database()
    yield
