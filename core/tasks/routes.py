from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_db
from tasks.schemas import *
from tasks.models import TaskModel

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_task_list(
        is_completed: bool = Query(None, description="filter tasks base on is_completed"),
        limit: int = Query(10, gt=0, le=50, description="limit tasks count"),
        offset: int = Query(0, ge=0, description="offset tasks count"),
        db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if is_completed is not None:
        query = query.filter_by(is_completed=is_completed)
    return query.offset(offset).limit(limit).all()


@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if task_obj:
        return task_obj
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
        request: TaskUpdateSchema,
        task_id: int = Path(..., gt=0),
        db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)

    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
