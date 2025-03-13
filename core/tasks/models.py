import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="tasks", uselist=False)
