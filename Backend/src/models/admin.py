from sqlalchemy import Column , String ,DateTime , ForeignKey , Integer , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username      = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tokens        = relationship("RefreshToken", back_populates="admin")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id   = Column(UUID(as_uuid=True), ForeignKey("admins.id"))
    token_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked    = Column(Boolean, default=False)
    admin      = relationship("Admin", back_populates="tokens")