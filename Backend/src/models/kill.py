from sqlalchemy import Column , String ,DateTime , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Kill(Base):
    __tablename__ = "kills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey("matches.id"), nullable=False)
    killer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    victim_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    weapon = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    match = relationship("Match", back_populates="kills")
    killer = relationship("User", foreign_keys=[killer_id])
    victim = relationship("User", foreign_keys=[victim_id])       