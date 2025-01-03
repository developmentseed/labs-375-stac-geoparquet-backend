from fastapi import FastAPI

import tistac.router

app = FastAPI()
app.include_router(tistac.router.router)
