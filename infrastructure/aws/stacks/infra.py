from typing import Any

from aws_cdk import (
    CfnOutput,
    Stack,
)
from config import Config
from constructs import Construct

from .constructs.bucket import Bucket


class InfraStack(Stack):
    def __init__(
        self, scope: Construct, config: Config, id: str, **kwargs: Any
    ) -> None:
        super().__init__(scope, id=id, tags=config.tags, **kwargs)

        self.bucket = Bucket(self, "bucket", config, region=self.region)
        CfnOutput(self, "BucketName", value=self.bucket.bucket.bucket_name)
