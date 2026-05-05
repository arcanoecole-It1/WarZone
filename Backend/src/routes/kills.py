from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.match import Match
from src.schemas.kill import KillCreate, KillResponse
from src.services.kill_service import record_kill

router = APIRouter(prefix="/kills", tags=["kills"])

@router.post("/", response_model=KillResponse, status_code=201)
async def create_kill(body: KillCreate, db: Session = Depends(get_db)):
    # Vérifie que la partie est bien en cours
    match = db.query(Match).filter_by(id=body.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    if match.status != "ongoing":
        raise HTTPException(status_code=409, detail="La partie est terminée")
    return await record_kill(body, db)