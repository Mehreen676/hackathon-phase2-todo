from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(SQLModel):
    title: str
    description: Optional[str] = None

class TaskRead(SQLModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
