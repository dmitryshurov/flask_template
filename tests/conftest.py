import pytest

from .helpers import clear_all_tables_in_database


@pytest.fixture(scope='session', autouse=True)
def clear_database():
    clear_all_tables_in_database()
    yield
    # clear_all_tables_in_database()
