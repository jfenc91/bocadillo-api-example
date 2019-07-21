# some fixtures for bocadillo
import pytest
from bocadillo import create_client, LiveServer
from asgi import app as vapp


@pytest.fixture
def app():
    return vapp


@pytest.fixture
def client(app):
    return create_client(app)


@pytest.fixture
def server(app):
    with LiveServer(app) as server:
        yield server
