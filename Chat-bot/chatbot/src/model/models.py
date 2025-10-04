from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid


class SessionCreate(BaseModel):
    pass

class SessionRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class MessageCreate(BaseModel):
    session_id: UUID
    role: str
    content: str

class MessageRead(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True


Base = declarative_base()

class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey('chat_sessions.id'), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)