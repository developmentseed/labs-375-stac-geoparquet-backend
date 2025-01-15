"""STACK Configs."""

from typing import Annotated, Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application settings"""

    name: str = "stac-fastapi-geoparquet"
    stage: str = "dev"
    owner: str = "labs-375"  # Add owner field for tracking
    project: str = "stac-fastapi-geoparquet"  # Add project field for tracking
    release: str = "dev"

    bucket_name: str = "stac-fastapi-geoparquet"
    geoparquet_key: Annotated[
        str, "storage key for the geoparquet file within the S3 bucket"
    ]

    timeout: int = 30
    memory: int = 3009

    # The maximum of concurrent executions you want to reserve for the function.
    # Default: - No specific limit - account limit.
    max_concurrent: Optional[int] = None

    # rate limiting settings
    rate_limit: Annotated[
        Optional[int],
        "maximum average requests per second over an extended period of time",
    ] = 10

    @property
    def stack_name(self) -> str:
        """Generate consistent resource prefix."""
        return f"{self.name}-{self.stage}"

    @property
    def tags(self) -> dict[str, str]:
        """Generate consistent tags for resources."""
        return {
            "Project": self.project,
            "Owner": self.owner,
            "Stage": self.stage,
            "Name": self.name,
            "Release": self.release,
        }

    class Config:
        """model config"""

        env_file = ".env"
        env_prefix = "STACK_"
