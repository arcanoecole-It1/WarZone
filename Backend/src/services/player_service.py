from datetime import datetime, timezone
from src.models.user import User
from src.models.player_stats import PlayerStats
from src.models.grade import Grade
from  src.schemas.player import PlayerCreate
from sqlalchemy.orm import Session

async def register_player(kill: PlayerCreate, db: Session) -> User:
    user = User(
        roblox_id  = kill.roblox_id,
        username   = kill.username,
        created_at = datetime.now(timezone.utc)
    )
    db.add(user)
    db.flush()
    db.add(PlayerStats(player_id=user.id))
    db.add(Grade(player_id=user.id, updated_at=datetime.now(timezone.utc)))
    db.commit()
    db.refresh(user)
    return user