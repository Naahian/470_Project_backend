from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from database import get_db
from routes import auth, users, items
from __init__ import create_tables, create_admin_user

app = FastAPI(
    title="FastAPI Auth API",
    description="A FastAPI application with JWT authentication and role-based access control",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

@app.on_event("startup")
def startup_event():
    """Initialize database and create admin user on startup"""
    create_tables()
    create_admin_user()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Auth API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)