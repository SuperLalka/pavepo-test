from typing import List, Type

from fastapi import HTTPException, UploadFile
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.models import Attachment
from src.repository.attachment_repository import AttachmentRepository
from src.schemas.attachment_schemas import AttachmentInput, AttachmentOutput
from src.service.user_service import UserService
from src.utils.utils import upload_file


class AttachmentService:

    def __init__(self, session: Session):
        self.repository = AttachmentRepository(session)

    async def create(self, data: AttachmentInput, file: UploadFile) -> AttachmentOutput:
        data.content = await upload_file(file)
        attachment = await self.repository.create(data)
        return AttachmentOutput(**attachment.model_dump(exclude_none=True))

    async def get_all(self) -> List[Type[Attachment]]:
        return await self.repository.get_all()

    async def get_all_by_user(self, user_id: UUID4) -> List[Type[Attachment]]:
        return await self.repository.get_all_by_user(user_id)

    async def delete(self, _id: UUID4) -> bool:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Attachment not found")

        attachment = await self.repository.get_by_id(_id)
        return await self.repository.delete(attachment)
