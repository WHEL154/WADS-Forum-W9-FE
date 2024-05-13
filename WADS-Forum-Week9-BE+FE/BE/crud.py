from sqlalchemy.orm import Session
from .models import Task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task_data):
    db_task = Task(title=task_data.title, status=task_data.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_data):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.title = task_data.title
        db_task.status = task_data.status
        db.commit()
        return db_task
    else:
        return None

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
