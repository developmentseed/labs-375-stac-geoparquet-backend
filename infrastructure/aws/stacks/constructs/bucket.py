from typing import Any

from aws_cdk import (
    RemovalPolicy,
)
from aws_cdk.aws_iam import AnyPrincipal, Effect, PolicyStatement
from aws_cdk.aws_s3 import BlockPublicAccess
from aws_cdk.aws_s3 import Bucket as AwsBucket
from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    AwsSdkCall,
    PhysicalResourceId,
)
from config import Config
from constructs import Construct


class Bucket(Construct):
    def __init__(
        self, scope: Construct, id: str, config: Config, region: str, **kwargs: Any
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.bucket = AwsBucket(
            scope=self,
            id="bucket",
            bucket_name=config.bucket_name,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
            if config.is_prod
            else RemovalPolicy.DESTROY,
            public_read_access=True,
            block_public_access=BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
        )

        # make the bucket public, requester-pays
        self.bucket.add_to_resource_policy(
            PolicyStatement(
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
                principals=[AnyPrincipal()],
                effect=Effect.ALLOW,
            )
        )

        add_request_pay = AwsSdkCall(
            action="putBucketRequestPayment",
            service="S3",
            region=region,
            parameters={
                "Bucket": self.bucket.bucket_name,
                "RequestPaymentConfiguration": {"Payer": "Requester"},
            },
            physical_resource_id=PhysicalResourceId.of(self.bucket.bucket_name),
        )

        aws_custom_resource = AwsCustomResource(
            self,
            "RequesterPaysCustomResource",
            policy=AwsCustomResourcePolicy.from_sdk_calls(
                resources=[self.bucket.bucket_arn]
            ),
            on_create=add_request_pay,
            on_update=add_request_pay,
        )

        aws_custom_resource.node.add_dependency(self.bucket)
