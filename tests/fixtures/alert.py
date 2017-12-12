import pytest
from hawkeye.alert import Alert

@pytest.fixture
def alert():
    return Alert('cpu', 20)
