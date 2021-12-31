import pytest


@pytest.fixture
def client():
    from src import server

    server.app.config['TESTING'] = True

    return server.app.test_client()
