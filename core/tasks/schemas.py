import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=5, description="Title of the Task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the Task")
    is_completed: bool = Field(..., description="State of the Task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique id of the Task")

    created_at: datetime.datetime = Field(..., description="Create time of the Task")
    updated_at: datetime.datetime = Field(..., description="Update time of the Task")
