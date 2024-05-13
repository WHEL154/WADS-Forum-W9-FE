from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    status: bool

class TaskCreate(TaskBase):
    
    pass

class Task(TaskBase):
    id: int  

    class Config:
        orm_mode = True
        
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    status: bool

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int  
    class Config:
        orm_mode = True
        