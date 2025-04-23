import os.path
from typing import Any

from aws_cdk import (
    Duration,
)
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpStage, ThrottleSettings
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_lambda import Code, Function, Handler, Runtime
from aws_cdk.aws_logs import RetentionDays
from config import Config
from constructs import Construct

from .bucket import Bucket


class GeoparquetApiLambda(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        config: Config,
        bucket: Bucket,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        api_lambda = Function(
            scope=self,
            id="lambda",
            runtime=Runtime.FROM_IMAGE,
            handler=Handler.FROM_IMAGE,
            memory_size=config.memory,
            log_retention=RetentionDays.ONE_WEEK,
            timeout=Duration.seconds(config.timeout),
            code=Code.from_asset_image(
                directory=os.path.abspath("."),
                file="infrastructure/aws/lambda/Dockerfile",
            ),
            environment={
                "STAC_FASTAPI_GEOPARQUET_HREF": f"s3://{config.bucket_name}/{config.geoparquet_key}",
            },
        )
        bucket.bucket.grant_read(api_lambda)
        api = HttpApi(
            scope=self,
            id="api",
            default_integration=HttpLambdaIntegration(
                "api-integration",
                handler=api_lambda,
            ),
            default_domain_mapping=None,  # TODO: enable custom domain name
            create_default_stage=False,  # Important: disable default stage creation
        )
        stage = HttpStage(
            self,
            "api-stage",
            http_api=api,
            auto_deploy=True,
            stage_name="$default",
            throttle=ThrottleSettings(
                rate_limit=config.rate_limit,
                burst_limit=config.rate_limit * 2,
            )
            if config.rate_limit
            else None,
        )
        self.url = stage.url
