from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime
    
    class Config:
        orm_mode = True
    

class UserReadList(BaseModel):
    users: list[UserRead]


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserCreatedReponse(BaseModel):
    id: int


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserPatch(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


