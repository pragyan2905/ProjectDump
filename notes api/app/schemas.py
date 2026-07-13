from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Auth Schemas ---
class UserBase(BaseModel):
    email: str # In production, use EmailStr from pydantic[email]

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Note Schemas ---
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
