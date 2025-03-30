from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.auth.validators import validate_email
from src.models import User
from src.repository.user_repository import UserRepository
from src.schemas.user_schemas import UserIn, UserInDBBase, UserOauthIn, UserUpdate


class UserService:

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    async def create(self, data: Union[UserIn, UserOauthIn]) -> UserInDBBase:
        if await self.repository.exists_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        validate_email(data.email)
        return await self.repository.create(data)

    async def is_exists(self, _id: str) -> bool:
        return await self.repository.exists_by_id(_id)

    async def get_by_id(self, _id: str) -> User:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")
        return await self.repository.get_by_id(_id)

    async def is_superuser(self, _id: str) -> bool:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")

        user = await self.repository.get_by_id(_id)
        return user.is_superuser

    async def update_user(self, _id: str, user_id: str, data: UserUpdate) -> UserInDBBase:
        if _id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")

        user = await self.repository.get_by_id(_id)
        return await self.repository.update_user(user, data)

    async def delete_user(self, _id: str, user_id: str) -> bool:
        if not await self.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")

        user = await self.repository.get_by_id(_id)
        await self.repository.delete_user(user)
        return True
