
from sqlalchemy import func, Boolean, Column, DateTime, String, inspect
from sqlalchemy.orm import relationship

from src.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, index=True, autoincrement=False)
    username = Column(String)
    real_name = Column(String)
    email = Column(String, unique=True, index=True)

    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_files = relationship("Attachment", back_populates="user")


user = inspect(User).local_table
