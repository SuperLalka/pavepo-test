from typing import Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user_schemas import UserIn, UserInDBBase


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserIn, hashed_password: str) -> UserInDBBase:
        db_user = User(**data.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.session.add(db_user)
        self.session.commit()
        # self.session.refresh(db_user)
        return UserInDBBase(**db_user.__dict__)

    def exists_by_id(self, _id: UUID4) -> bool:
        return self.session.query(User).filter(User.id == _id).first() is not None

    def exists_by_email(self, email: str) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None

    def exists_by_username(self, username: str) -> bool:
        return self.session.query(User).filter(User.username == username).first() is not None

    def get_by_id(self, _id: UUID4) -> Type[User]:
        return self.session.query(User).filter(User.id == _id).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def delete_user(self, user: Type[User]) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True
