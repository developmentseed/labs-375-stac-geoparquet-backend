from typing import Any

from aws_cdk.aws_ec2 import (
    GatewayVpcEndpointAwsService,
    InterfaceVpcEndpointAwsService,
    SubnetConfiguration,
    SubnetType,
)
from aws_cdk.aws_ec2 import (
    Vpc as CdkVpc,
)
from constructs import Construct


class Vpc(Construct):
    def __init__(
        self, scope: Construct, id: str, *, nat_gateway_count: int, **kwargs: Any
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = CdkVpc(
            self,
            "vpc",
            subnet_configuration=[
                SubnetConfiguration(
                    name="ingress", subnet_type=SubnetType.PUBLIC, cidr_mask=24
                ),
                SubnetConfiguration(
                    name="application",
                    subnet_type=SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                SubnetConfiguration(
                    name="rds",
                    subnet_type=SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                ),
            ],
            nat_gateways=nat_gateway_count,
        )
        self.vpc.add_interface_endpoint(
            "SecretsManagerEndpoint",
            service=InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
        )
        self.vpc.add_interface_endpoint(
            "CloudWatchEndpoint",
            service=InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
        )
        self.vpc.add_gateway_endpoint("S3", service=GatewayVpcEndpointAwsService.S3)

        scope.export_value(
            self.vpc.select_subnets(subnet_type=SubnetType.PUBLIC).subnets[0].subnet_id
        )
        scope.export_value(
            self.vpc.select_subnets(subnet_type=SubnetType.PUBLIC).subnets[1].subnet_id
        )
