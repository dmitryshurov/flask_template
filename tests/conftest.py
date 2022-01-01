import pytest

from .helpers import add_user_roles_to_database, clear_all_tables_in_database


@pytest.fixture(autouse=True)
def clear_database():
    clear_all_tables_in_database()
    add_user_roles_to_database()
    yield
