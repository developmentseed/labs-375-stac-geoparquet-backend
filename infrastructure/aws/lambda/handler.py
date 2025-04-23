"""AWS Lambda handler."""

import logging
import os
from pathlib import Path

import stac_fastapi.geoparquet.api
from mangum import Mangum
from rustac import DuckdbClient

logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
logging.getLogger("mangum.http").setLevel(logging.ERROR)

extension_directory = Path(os.environ["LAMBDA_TASK_ROOT"]) / "duckdb-extensions"

duckdb_client = DuckdbClient(
    install_spatial=False,
    use_hive_partitioning=False,
    extension_directory=extension_directory,
)
duckdb_client.execute("CREATE SECRET (TYPE S3, PROVIDER CREDENTIAL_CHAIN)")
api = stac_fastapi.geoparquet.api.create(duckdb_client=duckdb_client)
handler = Mangum(api.app, lifespan="on")
