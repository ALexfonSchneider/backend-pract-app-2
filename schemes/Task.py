from datetime import datetime
from pydantic import BaseModel, EmailStr

from schemes.User import UserRead


class TaskRead(BaseModel):
    id: int
    description: str
    user_id: int | None
    
    class Config:
        orm_mode = True
        

class TaskReadDetail(BaseModel):
    id: int
    description: str
    user: UserRead | None
    
    class Config:
        orm_mode = True


class TaskReadList(BaseModel):
    tasks: list[TaskRead]


class TaskCreate(BaseModel):
    user_id: int | None
    description: str


class TaskCreatedReponse(BaseModel):
    id: int


class TaskUpdate(BaseModel):
    description: str