import importlib.metadata

from fastapi import FastAPI

import tistac.dependencies
import tistac.router

settings = tistac.dependencies.get_settings()
app = FastAPI(
    title=settings.catalog_title or settings.catalog_id,
    description=settings.catalog_description,
    version=importlib.metadata.distribution("tistac").version,
)
app.include_router(tistac.router.router)
