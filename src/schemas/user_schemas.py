from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    id: str
    email: str
    is_superuser: bool = False
    is_active: bool = True


class UserIn(UserBase):
    real_name: Optional[str]
    username: Optional[str]


class UserOauthIn(UserBase):
    email: str = Field(validation_alias="default_email", serialization_alias="default_email")
    real_name: Optional[str] = None
    username: Optional[str] = Field(validation_alias="login", serialization_alias="login")


class UserOut(UserBase):
    real_name: Optional[str]
    username: Optional[str]


class UserInDBBase(UserBase):
    real_name: Optional[str]
    username: Optional[str]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str
