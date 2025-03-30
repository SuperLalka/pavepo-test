import uuid

from sqlalchemy import func, Column, DateTime, ForeignKey, String, inspect, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_file import File, FileField

from src.config.database import Base


class Attachment(Base):
    __tablename__ = "attachment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50))
    content = Column(FileField)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(String(), ForeignKey('users.id'))
    user = relationship("User", back_populates="user_files")

    __table_args__ = (
        UniqueConstraint("name", "user_id", name="user_attachments_idx"),
    )

    @property
    def content_storage_path(self):
        return self.content.path

    @property
    def content_url(self):
        return self.content.url


attachment = inspect(Attachment).local_table
