🧩 Hackathon II — Phase 2
Full-Stack Todo Application (CRUD)

This project implements a Phase-2 compliant full-stack Todo application using FastAPI for the backend and Next.js (App Router) for the frontend.

The focus of Phase-2 is:

Correct REST APIs

Database-backed CRUD

Frontend ↔ Backend integration

Clean deployment

No AI, agents, or chat functionality is included in this phase.

🧑‍⚖️ Note for Judges (Phase-2 Scope)

This submission is strictly scoped to Phase-2 requirements.

What to evaluate:

REST-based CRUD APIs

Database persistence

Frontend integration with backend

Correct API routing and deployment

Explicitly NOT included (by design):

OpenAI / Agents

Chatbot

Conversation memory

MCP tools
(These are implemented in Phase-3.)

✅ Features Implemented

Demo authentication (via localStorage user id)

Todo task management:

Add task

List tasks

Complete / toggle task

Delete task

Database persistence

Frontend dashboard with task controls

🖥️ Tech Stack
Frontend

Next.js (App Router)

Deployed on Vercel

Backend

FastAPI

SQLModel ORM

Database persistence

Deployed on Hugging Face Spaces

🌐 Live URLs
Frontend (Vercel)
https://mehreenasghar-todo.vercel.app/signin

Backend (FastAPI)
https://mehreenasghar5-todo-fastapi-backend.hf.space

📋 API Endpoints (Phase-2)

GET /api/{user_id}/tasks/

POST /api/{user_id}/tasks/

PATCH /api/{user_id}/tasks/{task_id}/complete

DELETE /api/{user_id}/tasks/{task_id}

These endpoints support full CRUD functionality for todo tasks.

🔧 Environment Variables
Frontend
NEXT_PUBLIC_API_BASE=https://mehreenasghar5-todo-fastapi-backend.hf.space

Backend
DATABASE_URL=your_database_url
ALLOWED_ORIGINS=https://mehreenasghar-todo.vercel.app

🏁 Final Status

✅ REST CRUD APIs implemented

✅ Database persistence working

✅ Frontend + backend fully integrated

✅ Deployed and accessible

❌ No AI / chatbot (intentionally excluded)

✅ Hackathon Phase-2: COMPLETE & COMPLIANT
