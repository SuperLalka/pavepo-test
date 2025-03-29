import logging

from fastapi import FastAPI, Response
from fastapi_oauth2.middleware import OAuth2Middleware, Auth
from fastapi_oauth2.router import router as oauth2_router
from sqlalchemy.orm import Session
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse

from src.auth.oauth import oauth2_config
from src.config.database import get_db
from src.config.settings import settings
from src.models.user import User
from src.router.api import router

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=settings.DEBUG,
)


def on_auth_success(auth: Auth, user: User):
    db: Session = next(get_db())
    query = db.query(User)
    if not query.filter_by(email=user.email).first():
        User(**{
            # "identity": user.identity,
            "username": user.get("username"),
            "name": user.display_name,
            "email": user.email,
        }).save(db)


def on_auth_error(conn: HTTPConnection, exc: Exception) -> Response:
    return JSONResponse({"detail": str(exc)}, status_code=400)


app.add_middleware(
    OAuth2Middleware,
    config=oauth2_config,
    callback=on_auth_success,
    on_error=on_auth_error,
)


@app.on_event("startup")
async def startup():
    app.include_router(router)
    app.include_router(oauth2_router)


@app.on_event("shutdown")
async def shutdown():
    pass
