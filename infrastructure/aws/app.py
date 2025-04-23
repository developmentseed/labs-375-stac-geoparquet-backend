"""AWS CDK application for the stac-fastapi-geoparquet stack, with a pgstac
database to compare."""

from aws_cdk import App
from config import Config
from stacks.app import AppStack
from stacks.infra import InfraStack

app = App()
config = Config()
infra_stack = InfraStack(
    scope=app,
    id=config.stack_name("infra"),
    config=config,
)
AppStack(
    scope=app,
    id=config.stack_name("app"),
    pgstac_db=infra_stack.pgstac_db,
    bucket=infra_stack.bucket,
    config=config,
)
app.synth()
