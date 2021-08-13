import os
import sys
import tempfile
from os.path import abspath
from os.path import dirname

import pytest
from fastapi.testclient import TestClient

# this is needed to the app and models modules can be imported when code is executed from within app
sys.path.append(dirname(dirname(abspath(__file__))))  # noqa !
from app.main import app

from alembic import command
from alembic.config import Config
from app.config import DB_FILE


pytest_plugins = "pytester"


@pytest.fixture()
def tempdir():
    with tempfile.TemporaryDirectory() as td:
        yield td


@pytest.fixture
def test_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # noqa
    config_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
    command.upgrade(Config(config_path), "heads")
    yield


@pytest.fixture
def client():
    client = TestClient(app)
    return client
