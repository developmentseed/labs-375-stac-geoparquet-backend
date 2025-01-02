from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pytest import FixtureRequest

import tistac.app
from tistac import Settings


@pytest.fixture(params=[str(Path(__file__).parents[1] / "data" / "naip.parquet")])
def client(request: FixtureRequest) -> TestClient:
    settings = Settings(backend=request.param)
    return TestClient(tistac.app.build(settings))
