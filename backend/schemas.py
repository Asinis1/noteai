from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime



class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None



class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class NoteCreate(BaseModel):
    title: str
    content: str
    folder: Optional[str] = "Genel"
    tags: Optional[List[str]] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    folder: Optional[str] = None
    tags: Optional[List[str]] = None


class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    keywords: Optional[str] = None
    folder: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagOut] = []

    class Config:
        from_attributes = True



class AIAnalysisRequest(BaseModel):
    note_id: int


class AIAnalysisResult(BaseModel):
    summary: str
    suggested_tags: List[str]
    keywords: List[str]