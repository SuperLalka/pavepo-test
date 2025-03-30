import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapi_oauth2.security import OAuth2

from src.config.database import get_db
from src.repository.attachment_repository import AttachmentRepository
from src.repository.user_repository import UserRepository
from src.schemas.attachment_schemas import AttachmentInDBBase

oauth2 = OAuth2()
router = APIRouter(
    prefix="/ssr"
)
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "json": json,
        "request": request,
    })


@router.get("/users", response_class=HTMLResponse)
@router.get("/users/", response_class=HTMLResponse, include_in_schema=False)
async def users(
    request: Request,
    _: str = Depends(oauth2),
    session: Session = Depends(get_db),
):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": [
            user.model_dump_json() for user
            in await UserRepository(session).get_all()
        ],
    })


@router.get("/attachments", response_class=HTMLResponse)
@router.get("/attachments/", response_class=HTMLResponse, include_in_schema=False)
async def attachments(
    request: Request,
    _: str = Depends(oauth2),
    session: Session = Depends(get_db),
):
    return templates.TemplateResponse("files.html", {
        "request": request,
        "files": [
            attach.__dict__ for attach
            in await AttachmentRepository(session).get_all()
        ],
    })
