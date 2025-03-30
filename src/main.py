import logging
import os

from fastapi import FastAPI
from fastapi_oauth2.middleware import OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from src.auth.oauth import oauth2_config
from src.auth.utils import on_auth_error, on_auth_success
from src.config.settings import settings
from src.router.api import router as router_api
from src.router.ssr import router as router_ssr

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=settings.DEBUG,
)

app.add_middleware(
    OAuth2Middleware,
    config=oauth2_config,
    callback=on_auth_success,
    on_error=on_auth_error,
)


# Configure Storage
os.makedirs("./upload_dir/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./upload_dir").get_container("attachment")
StorageManager.add_storage("default", container)

# Configure Static
app.mount("/static", StaticFiles(directory="static"))


@app.on_event("startup")
async def startup():
    app.include_router(router_api)
    app.include_router(router_ssr)
    app.include_router(oauth2_router)

    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url='/ssr')


@app.on_event("shutdown")
async def shutdown():
    pass
