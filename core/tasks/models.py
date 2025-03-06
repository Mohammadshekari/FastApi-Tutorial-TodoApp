import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, func, DateTime

from core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=True)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


