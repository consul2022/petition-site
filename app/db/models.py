from datetime import datetime

from db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)


class Petition(Base):
    __tablename__ = "petition"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=False)
    description = Column(Text, nullable=True, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False, default=datetime.utcnow)
    votes = Column(Integer, default=0)
    author_petition_id = Column(Integer, ForeignKey("user.id"))

    author_user = relationship("User")


class Vote(Base):
    __tablename__ = "vote"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    petition_id = Column(Integer, ForeignKey("petition.id"))
    timestamp = Column(DateTime, nullable=False, unique=False, default=datetime.utcnow)





