from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("")
def chat(user_id: str, payload: dict, session: Session = Depends(get_session)):
    msg = (payload.get("message") or "").strip()

    if not msg:
        raise HTTPException(status_code=400, detail="message is required")

    text = msg.lower()

    # ---------- LIST ----------
    if text == "list":
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        if not tasks:
            return {"reply": "No tasks found."}

        lines = []
        for t in tasks:
            status = "✅" if t.completed else "⬜"
            lines.append(f"{status} {t.id}: {t.title}")
        return {"reply": "\n".join(lines)}

    # ---------- PENDING ----------
    if text == "pending":
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id, Task.completed == False)
        ).all()
        if not tasks:
            return {"reply": "No pending tasks."}
        return {"reply": "\n".join([f"⬜ {t.id}: {t.title}" for t in tasks])}

    # ---------- COMPLETED ----------
    if text == "completed":
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id, Task.completed == True)
        ).all()
        if not tasks:
            return {"reply": "No completed tasks."}
        return {"reply": "\n".join([f"✅ {t.id}: {t.title}" for t in tasks])}

    # ---------- STATS ----------
    if text == "stats":
        total = session.exec(select(Task).where(Task.user_id == user_id)).all()
        done = [t for t in total if t.completed]
        return {
            "reply": f"Total: {len(total)}, Completed: {len(done)}, Pending: {len(total) - len(done)}"
        }

    # ---------- ADD (STRICT) ----------
    if text.startswith("add:"):
        content = msg[4:].strip()
        if not content:
            return {"reply": "Usage: add: title | optional description"}

        if "|" in content:
            title, desc = [x.strip() for x in content.split("|", 1)]
        else:
            title, desc = content, None

        task = Task(user_id=user_id, title=title, description=desc)
        session.add(task)
        session.commit()
        session.refresh(task)

        return {"reply": f"Added: {task.id}: {task.title}"}

    # ---------- COMPLETE ----------
    if text.startswith("complete:"):
        try:
            task_id = int(text.split(":")[1].strip())
        except ValueError:
            return {"reply": "Usage: complete: <id>"}

        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"reply": "Task not found."}

        task.completed = True
        session.add(task)
        session.commit()
        return {"reply": f"Completed: {task.id}: {task.title}"}

    # ---------- DELETE ----------
    if text.startswith("delete:"):
        try:
            task_id = int(text.split(":")[1].strip())
        except ValueError:
            return {"reply": "Usage: delete: <id>"}

        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"reply": "Task not found."}

        session.delete(task)
        session.commit()
        return {"reply": f"Deleted task {task_id}"}

    # ---------- FALLBACK ----------
    return {
        "reply": "Not Found. Use commands like: list, add: milk, complete: 1, delete: 1"
    }
