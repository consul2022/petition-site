from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class PetitionCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Petition(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
    votes: int
    author_user: User

    class Config:
        orm_mode = True

class Vote(BaseModel):
    id: int
    user_id: int
    petition_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
