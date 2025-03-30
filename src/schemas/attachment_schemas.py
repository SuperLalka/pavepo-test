from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, FilePath


class AttachmentBase(BaseModel):
    name: str


class AttachmentInput(AttachmentBase):
    content: Optional[FilePath] = None
    user_id: str


class AttachmentOutput(BaseModel):
    id: UUID4
    name: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class AttachmentInDBBase(AttachmentOutput):
    content: dict
