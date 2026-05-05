from sqlalchemy import Column , String ,DateTime , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Match(Base):
    __tablename__ = "matches"
    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    started_at  = Column(DateTime, nullable=False)
    ended_at    = Column(DateTime, nullable=True)
    winner_team = Column(String, nullable=True)
    map_name    = Column(String, nullable=False)
    status      = Column(String, nullable=False)
    duration   = Column(Integer, nullable=True) 
    kills       = relationship("Kill", back_populates="match")