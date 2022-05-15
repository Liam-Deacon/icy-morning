import pytest

from fastapi.testclient import TestClient
from app.api.routes import app


@pytest.fixture(scope='session')
def test_client() -> TestClient:
    yield TestClient(app)
