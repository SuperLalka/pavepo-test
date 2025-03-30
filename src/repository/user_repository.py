from typing import Type, List, Optional

from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user_schemas import UserIn, UserInDBBase, UserUpdate


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    async def create(self, data: UserIn) -> UserInDBBase:
        db_user = User(**data.model_dump())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserInDBBase(**db_user.__dict__)

    async def exists_by_id(self, _id: str) -> bool:
        return self.session.query(User).filter(User.id == _id).first() is not None

    async def exists_by_email(self, email: str) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None

    async def get_all(self) -> List[Optional[UserInDBBase]]:
        users = self.session.query(User).all()
        return self._map_city_to_schema_list(users)

    @staticmethod
    def _map_city_to_schema_list(users: List[Type[User]]) -> List[UserInDBBase]:
        return [
            UserInDBBase(**user.__dict__)
            for user in users
        ]

    async def get_by_id(self, _id: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == _id).first()

    async def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    async def update_user(self, user: Type[User], data: UserUpdate) -> UserInDBBase:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(user, key, value)

        self.session.commit()
        self.session.refresh(user)
        return UserInDBBase(**user.__dict__)

    async def delete_user(self, user: Type[User]) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True
