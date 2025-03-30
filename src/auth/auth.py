from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.config.settings import settings
from src.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    # try:
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )

    _id: str = payload.get("id")
    assert _id is not None

    user = db.query(User).filter(User.id == _id).first()
    assert user is not None

    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Could not validate JWT")
    # except AssertionError:
    #     raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user
