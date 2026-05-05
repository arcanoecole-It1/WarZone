from src.models.match import Match
from src.models.kill import Kill
from src.schemas.match import MatchCreate, MatchClose
from src.models.player_stats import PlayerStats
from uuid import UUID
from sqlalchemy.orm import Session

async def create_match(kill: MatchCreate, db: Session) -> Match:
    match = Match(map_name=kill.map_name, started_at=kill.started_at, status="ongoing")
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

async def close_match(match_id: UUID, kill: MatchClose, db: Session) -> Match:
    match = db.query(Match).filter_by(id=match_id).first()
    match.winner_team = kill.winner_team
    match.ended_at    = kill.ended_at
    match.status      = "finished"
    _update_win_rates(match_id, kill.winner_team, db)
    db.commit()
    db.refresh(match)
    return match

def _update_win_rates(match_id, winner_team, db):
    kills = db.query(Kill).filter_by(match_id=match_id).all()
    winner_ids = {k.killer_id for k in kills if k.winner_team == winner_team}
    for player_id in {k.killer_id for k in kills}:
        stats = db.query(PlayerStats).filter_by(player_id=player_id).first()
        stats.total_matches += 1
        if player_id in winner_ids: stats.total_wins += 1
        stats.win_rate = round(stats.total_wins / stats.total_matches * 100, 1)