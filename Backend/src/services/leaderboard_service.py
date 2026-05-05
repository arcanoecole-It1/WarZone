from sqlalchemy.orm import Session
from src.models.player_stats import PlayerStats

def get_top_players(db: Session, limit: int, sort_by: str) -> list:
    col = getattr(PlayerStats, sort_by)
    return db.query(PlayerStats).order_by(col.desc()).limit(limit).all()