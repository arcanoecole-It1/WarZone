from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.analytics import OverviewResponse, WeaponStat, DailyStat
from src.services.analytics_service import get_overview, kills_by_weapon, matches_per_day
from src.auth.jwt import CurrentAdmin

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview", response_model=OverviewResponse)
def overview(admin: CurrentAdmin, db: Session = Depends(get_db)):
    return get_overview(db)

@router.get("/kills-by-weapon", response_model=list[WeaponStat])
def by_weapon(admin: CurrentAdmin, db: Session = Depends(get_db)):
    return kills_by_weapon(db)

@router.get("/matches-per-day", response_model=list[DailyStat])
def per_day(admin: CurrentAdmin, db: Session = Depends(get_db)):
    return matches_per_day(db)