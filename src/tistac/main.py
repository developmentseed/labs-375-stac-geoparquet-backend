import importlib.metadata

from fastapi import FastAPI

import tistac.router

app = FastAPI(
    version=importlib.metadata.distribution("tistac").version,
)
app.include_router(tistac.router.router)
