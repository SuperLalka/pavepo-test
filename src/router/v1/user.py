from typing import List

from fastapi import APIRouter, Depends, Request, Body
from sqlalchemy.orm import Session

from src.auth.auth import get_current_user
from src.auth.decorators import has_permissions
from src.auth.permissions import IsSuperAdmin
from src.config.database import get_db
from src.schemas.attachment_schemas import AttachmentInDBBase
from src.schemas.user_schemas import UserIn, UserOut, UserUpdate
from src.service.attachment_service import AttachmentService
from src.service.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("", status_code=200)
@router.get("/", status_code=200, include_in_schema=False)
async def get_me(
    request: Request,
    current_user: UserIn = Depends(get_current_user)
):
    return current_user


@router.patch("/{user_id}", response_model=UserOut)
@router.patch(
    "/{user_id}/",
    response_model=UserOut,
    include_in_schema=False,
)
async def update_user(
    request: Request,
    user_id: str,
    current_user: UserIn = Depends(get_current_user),
    user_data: UserUpdate = Body(...),
    session: Session = Depends(get_db)
):
    return await UserService(session).update_user(current_user.id, user_id, user_data)


@router.delete("/{user_id}", status_code=204)
@router.delete("/{user_id}/", status_code=204, include_in_schema=False)
@has_permissions(IsSuperAdmin)
async def delete_user(
        request: Request,
        user_id: str,
        current_user: UserIn = Depends(get_current_user),
        session: Session = Depends(get_db)
):
    return await UserService(session).delete_user(current_user.id, user_id)


@router.get("/{user_id}/files", response_model=List[AttachmentInDBBase])
@router.get("/{user_id}/files/", response_model=List[AttachmentInDBBase], include_in_schema=False)
@has_permissions(IsSuperAdmin)
async def user_files(
        request: Request,
        user_id: str,
        session: Session = Depends(get_db)
):
    return await AttachmentService(session).get_all_by_user(user_id)
