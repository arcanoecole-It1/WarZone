from sqlalchemy import Column , String ,DateTime 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class User(Base):
    __tablename__ = "users"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roblox_id  = Column(String, unique=True, nullable=False)
    username   = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    stats      = relationship("PlayerStats", back_populates="user", uselist=False)
    grade      = relationship("Grade", back_populates="user", uselist=False)

    @property
    def win_rate(self) -> float:
        return float(self.stats.win_rate) if self.stats else 0.0