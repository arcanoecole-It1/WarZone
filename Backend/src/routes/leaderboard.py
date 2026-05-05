from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.stats import StatsResponse
from src.services.leaderboard_service import get_top_players
from src.auth.jwt import CurrentAdmin

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=list[StatsResponse])
def leaderboard(
    admin:    CurrentAdmin,  # protégé : dashboard uniquement
    db:       Session = Depends(get_db),
    limit:    int = Query(default=10, ge=1, le=100),
    sort_by:  str = Query(default="total_kills", pattern="^(total_kills|kd_ratio|win_rate)$"),
):
    return get_top_players(db, limit=limit, sort_by=sort_by)