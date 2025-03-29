from typing import Type, List, Optional

from pydantic import UUID4
from sqlalchemy.orm import Session

from src.models.attachment import Attachment
from src.schemas.attachment_schemas import AttachmentInput, AttachmentOutput


class AttachmentRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: AttachmentInput) -> AttachmentOutput:
        db_attachment = Attachment(**data.model_dump(exclude_none=True))
        self.session.add(db_attachment)
        self.session.commit()
        return AttachmentOutput(**db_attachment.__dict__)

    def exists_by_id(self, _id: UUID4) -> bool:
        return self.session.query(Attachment).filter(Attachment.id == _id).first() is not None

    def get_by_id(self, _id: UUID4) -> Type[Attachment]:
        return self.session.query(Attachment).filter(Attachment.id == _id).first()

    def get_all(self) -> List[Optional[AttachmentOutput]]:
        attachments = self.session.query(Attachment).all()
        return self._map_city_to_schema_list(attachments)

    def get_all_by_user(self, user_id: UUID4) -> List[Optional[AttachmentOutput]]:
        attachments = self.session.query(Attachment).filter_by(user_id=user_id).all()
        return self._map_city_to_schema_list(attachments)

    @staticmethod
    def _map_city_to_schema_list(attachments: List[Type[Attachment]]) -> List[AttachmentOutput]:
        return [
            AttachmentOutput(
                id=attach.id,
                name=attach.name,
            )
            for attach in attachments
        ]

    def delete(self, offer: Type[Attachment]) -> bool:
        self.session.delete(offer)
        self.session.commit()
        return True
