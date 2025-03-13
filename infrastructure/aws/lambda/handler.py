"""AWS Lambda handler."""

import logging
import os
import shutil

from mangum import Mangum
from stac_fastapi.geoparquet.main import app

if not os.path.exists("/tmp/duckdb-extensions") and os.path.isdir("/duckdb-extensions"):
    shutil.copytree("/duckdb-extensions", "/tmp/duckdb-extensions")

logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
logging.getLogger("mangum.http").setLevel(logging.ERROR)

handler = Mangum(app, lifespan="on")
