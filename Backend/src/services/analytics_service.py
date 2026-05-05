from sqlalchemy.orm import Session
from src.models.kill import Kill
from src.models.match import Match
from src.models.user import User
from sqlalchemy import func

def get_overview(db: Session) -> dict:
    return {
        "total_kills":    db.query(Kill).count(),
        "total_matches":  db.query(Match).count(),
        "active_players": db.query(User).count(),
    }

def kills_by_weapon(db: Session) -> list:
    from sqlalchemy import func
    rows = db.query(Kill.weapon, func.count().label("count"))\
             .group_by(Kill.weapon).order_by(func.count().desc()).all()
    return [{"weapon": r.weapon, "count": r.count} for r in rows]

def matches_per_day(db: Session) -> list:
    rows = db.query(
        func.date(Match.started_at).label("date"),
        func.count().label("matches")
    ).group_by(func.date(Match.started_at))\
     .order_by(func.date(Match.started_at)).all()
    return [{"date": str(r.date), "matches": r.matches} for r in rows]