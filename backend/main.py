from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.database import engine
from app import models  # noqa
from app.router.tasks import router as tasks_router

app = FastAPI(title="Hackathon Todo API")

# ✅ CORS (Frontend ↔ Backend allow)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(tasks_router)

@app.get("/health")
def health():
    return {"status": "ok"}
