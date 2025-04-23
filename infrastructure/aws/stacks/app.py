from typing import Any

from aws_cdk import (
    CfnOutput,
    Stack,
)
from config import Config
from constructs import Construct
from eoapi_cdk import PgStacApiLambda, PgStacDatabase

from .constructs.bucket import Bucket
from .constructs.geoparquet_api_lambda import GeoparquetApiLambda


class AppStack(Stack):
    def __init__(
        self,
        scope: Construct,
        pgstac_db: PgStacDatabase,
        bucket: Bucket,
        id: str,
        config: Config,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            scope,
            id=id,
            tags=config.tags,
            **kwargs,
        )

        pgstac_api = PgStacApiLambda(
            self,
            "pgstac-api",
            api_env={
                "NAME": "stac-fastapi-pgstac",
                "description": f"{config.project} STAC API",
            },
            db=pgstac_db.connection_target,
            db_secret=pgstac_db.pgstac_secret,
            stac_api_domain_name=None,
        )
        assert pgstac_api.url
        CfnOutput(self, "PgstacApiURL", value=pgstac_api.url)

        geoparquet_api = GeoparquetApiLambda(
            self, "geoparquet-api", config=config, bucket=bucket
        )
        assert geoparquet_api.url
        CfnOutput(self, "GeoparquetApiURL", value=geoparquet_api.url)
