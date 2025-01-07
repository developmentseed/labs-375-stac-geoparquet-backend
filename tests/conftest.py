from pathlib import Path
from typing import AsyncIterator

import pytest
from fastapi.testclient import TestClient

import stac_fastapi.geoparquet.main

naip_items = Path(__file__).parents[1] / "data" / "naip.parquet"


@pytest.fixture()
async def client() -> AsyncIterator[TestClient]:
    with TestClient(stac_fastapi.geoparquet.main.app) as client:
        yield client
