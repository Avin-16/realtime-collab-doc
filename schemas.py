from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class ShowUser(BaseModel):
    id:int
    name :str
    email : EmailStr

    class Config:
        orm_mode = True

class UploadedFileResponse(BaseModel):
    id: UUID
    file_name: str
    url: str
    size: int
    uploaded_at: datetime

    class Config:
        orm_mode = True