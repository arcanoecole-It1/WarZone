from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.player_stats import PlayerStats
from src.models.grade import Grade
from src.schemas.stats import StatsResponse, GradeResponse
from src.auth.jwt import CurrentAdmin

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/{player_id}", response_model=StatsResponse)
def get_stats(player_id: str, db: Session = Depends(get_db)):
    # Route publique : accessible depuis Roblox et le dashboard
    stats = db.query(PlayerStats).filter_by(player_id=player_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Stats introuvables")
    return stats


@router.get("/{player_id}/grade", response_model=GradeResponse)
def get_grade(player_id: str, db: Session = Depends(get_db)):
    grade = db.query(Grade).filter_by(player_id=player_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade introuvable")
    return grade