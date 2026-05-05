from sqlalchemy import Column , String , ForeignKey , Integer , Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class PlayerStats(Base):
    __tablename__ = "player_stats"
    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    total_kills  = Column(Integer, default=0)
    total_deaths = Column(Integer, default=0)
    kd_ratio     = Column(Float, default=0.0)
    total_wins   = Column(Integer, default=0)
    total_matches= Column(Integer, default=0)
    win_rate     = Column(Float, default=0.0)
    user         = relationship("User", back_populates="stats")

    @property
    def kill_totals(self) -> int:
        return self.total_kills