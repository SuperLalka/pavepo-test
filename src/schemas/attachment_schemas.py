from datetime import datetime

from pydantic import BaseModel, UUID4
from sqlalchemy_file import File


class AttachmentInput(BaseModel):
    name: str
    content: File
    user_id: UUID4


class AttachmentOutput(BaseModel):
    id: UUID4
    name: str
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
