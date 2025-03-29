from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.auth.security import create_access_token, get_password_hash, pwd_context
from src.auth.validators import validate_email, validate_password
from src.config.settings import settings
from src.repository.user_repository import UserRepository
from src.schemas.user_schemas import UserIn, UserInDBBase


class UserService:

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def create(self, data: UserIn) -> UserInDBBase:
        if self.repository.exists_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.repository.exists_by_username(data.username):
            raise HTTPException(status_code=400, detail="Username already registered")

        validate_password(data.password)
        validate_email(data.email)

        hashed_password = get_password_hash(data.password)
        user = self.repository.create(data, hashed_password)
        return user

    def login(self, data: OAuth2PasswordRequestForm) -> dict:
        user = self.repository.get_by_username(data.username)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    def is_superuser(self, _id: UUID4) -> bool:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")

        user = self.repository.get_by_id(_id)
        return user.is_superuser

    def delete_user(self, _id: UUID4, user_id: UUID4) -> bool:
        if not self.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="User not found")

        user = self.repository.get_by_id(_id)
        self.repository.delete_user(user)
        return True
