from fastapi_oauth2.middleware import Auth, User
from sqlalchemy.orm import Session
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse

from src.config.database import get_db
from src.schemas.user_schemas import UserOauthIn
from src.service.user_service import UserService


async def on_auth_success(auth: Auth, user: User) -> None:
    db: Session = next(get_db())
    if not await UserService(db).is_exists(user.id):
        user = UserOauthIn(**user)
        await UserService(db).create(user)


async def on_auth_error(conn: HTTPConnection, exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": str(exc)}, status_code=400)
