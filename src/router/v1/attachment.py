from typing import List

from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.auth.auth import get_current_user
from src.config.database import get_db
from src.schemas.attachment_schemas import AttachmentInput, AttachmentOutput, AttachmentInDBBase
from src.schemas.user_schemas import UserIn
from src.service.attachment_service import AttachmentService

router = APIRouter(
    prefix="/attachments",
    tags=["attachments"]
)


@router.get("/my", response_model=List[AttachmentInDBBase])
@router.get("/my/", response_model=List[AttachmentInDBBase], include_in_schema=False)
async def user_files(
    request: Request,
    current_user: UserIn = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    return await AttachmentService(session).get_all_by_user(current_user.id)


@router.post("/upload", response_model=AttachmentOutput)
@router.post("/upload/", response_model=AttachmentOutput, include_in_schema=False)
async def upload(
    request: Request,
    name: str = Form(...),
    file: UploadFile = File(...),
    current_user: UserIn = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    file.filename = name

    return await AttachmentService(session).create(
        AttachmentInput(
            name=name,
            user_id=current_user.id,
        ),
        file
    )
