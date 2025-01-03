from pathlib import Path
from typing import AsyncIterator

import pytest
import stacrs
from fastapi.testclient import TestClient
from pgstacrs import Client
from pypgstac.db import PgstacDB
from pypgstac.migrate import Migrate
from pystac import Collection, Extent, Item
from pytest import FixtureRequest
from pytest_postgresql import factories
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.janitor import DatabaseJanitor

from tistac import Settings
from tistac.dependencies import get_settings

naip_items = Path(__file__).parents[1] / "data" / "naip.parquet"
pgstac_proc = factories.postgresql_proc()


@pytest.fixture(scope="session")
async def pgstac(pgstac_proc: PostgreSQLExecutor) -> AsyncIterator[PostgreSQLExecutor]:
    dsn = f"postgresql://{pgstac_proc.user}:{pgstac_proc.password}@{pgstac_proc.host}:{pgstac_proc.port}/{pgstac_proc.template_dbname}"
    pgstac_db = PgstacDB(dsn)
    Migrate(pgstac_db).run_migration()
    items = stacrs.read(str(naip_items))["features"][
        0:100
    ]  # pgstac takes too long to load 10000 items
    extent = Extent.from_items((Item.from_dict(d) for d in items))
    collection = Collection(
        id="naip", description="Test NAIP collection", extent=extent
    )
    client = await Client.open(dsn)
    await client.create_collection(
        collection.to_dict(include_self_link=False, transform_hrefs=False)
    )
    await client.create_items(items)
    yield pgstac_proc


@pytest.fixture(params=["stac-geoparquet", "pgstac"])
async def client(
    request: FixtureRequest, pgstac: PostgreSQLExecutor
) -> AsyncIterator[TestClient]:
    from tistac.main import app

    if request.param == "stac-geoparquet":

        def get_settings_override() -> Settings:
            return Settings(backend=str(naip_items))

        app.dependency_overrides[get_settings] = get_settings_override
        yield TestClient(app)
    elif request.param == "pgstac":
        with DatabaseJanitor(
            user=pgstac.user,
            host=pgstac.host,
            port=pgstac.port,
            version=pgstac.version,
            password=pgstac.password,
            dbname="pypgstac_test",
            template_dbname=pgstac.template_dbname,
        ) as database_janitor:

            def get_settings_override() -> Settings:
                return Settings(
                    backend=f"postgresql://{database_janitor.user}:{database_janitor.password}@{database_janitor.host}:{database_janitor.port}/{database_janitor.dbname}"
                )

            app.dependency_overrides[get_settings] = get_settings_override
            yield TestClient(app)
    else:
        raise Exception(f"Unknown backend type: {request.param}")
