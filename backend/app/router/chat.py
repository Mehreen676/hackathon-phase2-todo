from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import engine
from app.models import Task

router = APIRouter(prefix="/api", tags=["chat"])


class ChatIn(BaseModel):
    message: str


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _get_tasks(session: Session, user_id: str):
    stmt = select(Task).where(Task.user_id == user_id)
    return session.exec(stmt).all()


@router.post("/{user_id}/chat")
def chat_handler(user_id: str, payload: ChatIn):
    msg = _norm(payload.message)

    with Session(engine) as session:
        # LIST
        if msg in ["list", "tasks", "list tasks", "show tasks", "all tasks"]:
            tasks = _get_tasks(session, user_id)
            if not tasks:
                return {"reply": "No tasks found."}
            lines = [f"{t.id} | {'✅' if t.completed else '⏳'} | {t.title}" for t in tasks]
            return {"reply": "Tasks:\n" + "\n".join(lines)}

        # PENDING
        if msg in ["pending", "pending tasks", "show pending"]:
            tasks = [t for t in _get_tasks(session, user_id) if not t.completed]
            if not tasks:
                return {"reply": "No pending tasks."}
            lines = [f"{t.id} | ⏳ | {t.title}" for t in tasks]
            return {"reply": "Pending:\n" + "\n".join(lines)}

        # COMPLETED
        if msg in ["completed", "completed tasks", "show completed"]:
            tasks = [t for t in _get_tasks(session, user_id) if t.completed]
            if not tasks:
                return {"reply": "No completed tasks."}
            lines = [f"{t.id} | ✅ | {t.title}" for t in tasks]
            return {"reply": "Completed:\n" + "\n".join(lines)}

        # STATS
        if msg in ["stats", "summary"]:
            tasks = _get_tasks(session, user_id)
            total = len(tasks)
            done = len([t for t in tasks if t.completed])
            return {"reply": f"Total: {total}, Completed: {done}, Pending: {total - done}"}

        # ADD: add: Title | optional description
        if msg.startswith("add:") or msg.startswith("add "):
            raw = payload.message.split(":", 1)[1].strip() if ":" in payload.message else payload.message[4:].strip()
            title, desc = (raw.split("|", 1) + [""])[:2]
            title = title.strip()
            desc = desc.strip() or None
            if not title:
                return {"reply": "Add format: add: Title | optional description"}

            task = Task(user_id=user_id, title=title, description=desc)
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"reply": f"Added: {task.id} | {task.title}"}

        # COMPLETE: complete: <id> (toggle)
        if msg.startswith("complete:") or msg.startswith("done:"):
            raw = payload.message.split(":", 1)[1].strip()
            if not raw.isdigit():
                return {"reply": "Complete format: complete: <id>"}
            task = session.get(Task, int(raw))
            if not task or task.user_id != user_id:
                return {"reply": "Task not found (id)."}
            task.completed = not task.completed
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"reply": f"Toggled: {task.id} | {task.title}"}

        # DELETE: delete: <id>
        if msg.startswith("delete:") or msg.startswith("remove:"):
            raw = payload.message.split(":", 1)[1].strip()
            if not raw.isdigit():
                return {"reply": "Delete format: delete: <id>"}
            task = session.get(Task, int(raw))
            if not task or task.user_id != user_id:
                return {"reply": "Task not found (id)."}
            session.delete(task)
            session.commit()
            return {"reply": f"Deleted: {raw}"}

        return {
            "reply": (
                "Commands:\n"
                "- list / pending / completed\n"
                "- add: Title | optional description\n"
                "- complete: <id>\n"
                "- delete: <id>\n"
                "- stats"
            )
        }
