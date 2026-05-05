from sqlalchemy.orm import Session
from src.models.kill import Kill
from src.schemas.kill import KillCreate
from src.models.player_stats import PlayerStats
from src.models.grade import Grade
from datetime import datetime, timezone

async def record_kill(kill: KillCreate, db: Session) -> Kill:
    new_kill = Kill(
        killer_id = kill.killer_id,
        victim_id = kill.victim_id,
        match_id  = kill.match_id,
        weapon    = kill.weapon,
        timestamp = kill.timestamp
    )
    db.add(new_kill)
    db.flush()
    killer_stats = db.query(PlayerStats).filter_by(player_id=kill.killer_id).first()
    victim_stats = db.query(PlayerStats).filter_by(player_id=kill.victim_id).first()
    killer_stats.total_kills  += 1
    victim_stats.total_deaths += 1
    killer_stats.kd_ratio = round(
        killer_stats.total_kills / max(killer_stats.total_deaths, 1), 2
    )
    await _update_grade(kill.killer_id, killer_stats.total_kills, db)
    db.commit()
    db.refresh(new_kill)
    return new_kill

async def _update_grade(player_id, total_kills: int, db: Session):
    grade = db.query(Grade).filter_by(player_id=player_id).first()
    if   total_kills >= 500: grade.label, grade.level = "Legendary", 5
    elif total_kills >= 200: grade.label, grade.level = "Diamond",  4
    elif total_kills >= 100: grade.label, grade.level = "Gold",     3
    elif total_kills >=  50: grade.label, grade.level = "Silver",   2
    else:                   grade.label, grade.level = "Bronze",   1
    grade.updated_at = datetime.now(timezone.utc)