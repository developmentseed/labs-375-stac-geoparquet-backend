from typing import Any

from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from aws_cdk.aws_ec2 import (
    InstanceType,
    Peer,
    Port,
    SubnetSelection,
    SubnetType,
)
from aws_cdk.aws_rds import DatabaseInstanceEngine, PostgresEngineVersion
from config import Config
from constructs import Construct
from eoapi_cdk import PgStacDatabase

from .constructs.bucket import Bucket
from .constructs.vpc import Vpc


class InfraStack(Stack):
    def __init__(
        self, scope: Construct, config: Config, id: str, **kwargs: Any
    ) -> None:
        super().__init__(scope, id=id, tags=config.tags, **kwargs)

        self.vpc = Vpc(self, "vpc", nat_gateway_count=config.nat_gateway_count)

        self.pgstac_db = PgStacDatabase(
            self,
            "pgstac-db",
            vpc=self.vpc.vpc,
            engine=DatabaseInstanceEngine.postgres(
                version=PostgresEngineVersion.VER_16
            ),
            vpc_subnets=SubnetSelection(subnet_type=(SubnetType.PUBLIC)),
            allocated_storage=config.pgstac_db_allocated_storage,
            instance_type=InstanceType(config.pgstac_db_instance_type),
            removal_policy=(
                RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
                if config.is_prod
                else RemovalPolicy.DESTROY
            ),
        )
        # allow connections from any ipv4 to pgbouncer instance security group
        assert self.pgstac_db.security_group
        self.pgstac_db.security_group.add_ingress_rule(Peer.any_ipv4(), Port.tcp(5432))

        self.bucket = Bucket(self, "bucket", config, region=self.region)
        CfnOutput(self, "BucketName", value=self.bucket.bucket.bucket_name)
