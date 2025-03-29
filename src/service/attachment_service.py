from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.repository.attachment_repository import AttachmentRepository
from src.schemas.attachment_schemas import AttachmentInput, AttachmentOutput
from src.service.user_service import UserService


class AttachmentService:

    def __init__(self, session: Session):
        self.repository = AttachmentRepository(session)
        self.user_service = UserService(session)

    def create(self, data: AttachmentInput) -> AttachmentOutput:
        attachment = self.repository.create(data)
        return AttachmentOutput(**attachment.model_dump(exclude_none=True))

    def get_all(self) -> List[AttachmentOutput]:
        return self.repository.get_all()

    def get_all_by_user(self, user_id: UUID4) -> List[AttachmentOutput]:
        return self.repository.get_all_by_user(user_id)

    def delete(self, _id: UUID4) -> bool:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Attachment not found")

        attachment = self.repository.get_by_id(_id)
        return self.repository.delete(attachment)
