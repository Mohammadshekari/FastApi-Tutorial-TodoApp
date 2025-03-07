import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, func, DateTime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from core.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(250), nullable=False)
    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    tasks = relationship("TaskModel", back_populates="user", )

    def verify_password(self, plain_password: str) -> bool:
        return Hasher.verify_password(plain_password, self.password)
