from sqlalchemy import Column , String ,DateTime , ForeignKey , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Grade(Base):
    __tablename__ = "grades"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id  = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    label      = Column(String, default="Bronze")
    level      = Column(Integer, default=1)
    updated_at = Column(DateTime)
    user       = relationship("User", back_populates="grade")