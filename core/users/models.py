import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, func, DateTime
from sqlalchemy.orm import relationship

from core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(250), nullable=False)
    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

