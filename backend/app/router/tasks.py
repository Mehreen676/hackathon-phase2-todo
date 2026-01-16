from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def list_tasks(user_id: str, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    user_id: str,
    payload: TaskCreate,
    session: Session = Depends(get_session),
):
    task = Task(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: int,
    payload: TaskUpdate,
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = payload.title
    task.description = payload.description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"status": "deleted", "id": task_id}


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
