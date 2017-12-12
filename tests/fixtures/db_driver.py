import pytest
from hawkeye.utils.db_drivers.postgres_driver import PostgresDriver
from hawkeye import settings

@pytest.fixture
def db_driver():
    return PostgresDriver(**settings.DB_CREDENTIALS)
