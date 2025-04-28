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

        if geoparquet_api.domain_name:
            CfnOutput(
                self,
                "ApiGatewayDomainNameTarget",
                value=geoparquet_api.domain_name.regional_domain_name,
                description="The target for the CNAME/ALIAS record",
            )
            CfnOutput(
                self,
                "GeoparquetApiURL",
                value=f"https://{geoparquet_api.domain_name.name}",
                description="The custom domain URL for the API",
            )
        else:
            assert geoparquet_api.stage.url
            CfnOutput(
                self,
                "GeoparquetApiURL",
                value=geoparquet_api.stage.url,
                description="The default stage URL for the API",
            )
