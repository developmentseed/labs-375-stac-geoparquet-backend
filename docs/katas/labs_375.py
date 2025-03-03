"""Common configuration that's used in our katas."""

from __future__ import annotations

import time
from types import TracebackType
from typing import Any

STAC_FASTAPI_GEOPARQUET_URI = "https://4y16a90iwk.execute-api.us-west-2.amazonaws.com/"
NAIP_GEOPARQUET_URI = "s3://stac-fastapi-geoparquet-devseed/naip.parquet"


class Timer:
    """A simple class for timing how long it takes to get a bunch of items."""

    def __enter__(self) -> Timer:
        self._start = time.time()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def report(self, items: list[dict[str, Any]]) -> None:
        stop = time.time()
        rate = len(items) / (stop - self._start)
        print(
            f"Retrieved {len(items)} in {(stop - self._start):0.2f}s "
            f"({rate:0.2f} items/s)"
        )
