import pytest
from fastapi.testclient import TestClient

import tistac.app


@pytest.fixture
def client() -> TestClient:
    return TestClient(tistac.app.build())
