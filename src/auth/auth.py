from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth import security
from config.database import get_db
from models.user import User
from schemas.user import TokenData

from src.router.exceptions import unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub")
        assert username is not None

        token_data = TokenData(username=username)
        user = db.query(User).filter(User.username == token_data.username).first()
        assert user is not None

    except JWTError:
        return unauthorized("Could not validate JWT")
    except AssertionError:
        return unauthorized("Could not validate credentials")

    return user
