from sqlalchemy import Column, Integer, String , DateTime, ForeignKey
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)


class Document(Base):
    __tablename__ = "uploaded_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(255), nullable=False)
    content_type = Column(String(100))
    size = Column(Integer)
    path = Column(String(500))
    uploaded_by = Column(String(100))  # could link to user.id in real use
    created_at = Column(DateTime(timezone=True), server_default=func.now())