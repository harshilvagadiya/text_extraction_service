from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from src.repository.table import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    documents = relationship("Document", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=True)
    file_format = Column(Enum("pdf", "doc", "docx", name="file_formats"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    extracted_text = Column(Text, nullable=True)
    extraction_status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    user_id = Column(Integer, ForeignKey("users.id"))    
    owner = relationship("User", back_populates="documents")
