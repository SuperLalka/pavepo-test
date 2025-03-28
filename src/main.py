import logging

from fastapi import FastAPI

import database

from src.config import settings
from src.router.api import router

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    redoc_url="/api/v1/redoc",
    docs_url="/api/v1/docs",
    debug=settings.Settings.debug,
)


app.add_middleware(database.DBSessionMiddleware)


@app.on_event("startup")
async def startup():
    app.include_router(router)


@app.on_event("shutdown")
async def shutdown():
    await database.engine.dispose()
