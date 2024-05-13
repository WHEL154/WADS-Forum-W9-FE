from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine, Base
from .models import Task as TaskModel
from .crud import get_tasks, get_task, create_task, update_task, delete_task
from .schemas import TaskCreate, Task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/", response_model=Task, status_code=201)
async def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@app.put("/tasks/{task_id}", response_model=Task)
async def modify_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    updated_task = update_task(db, task_id, task_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def remove_task(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

