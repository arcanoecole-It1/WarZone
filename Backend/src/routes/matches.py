from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.match import Match
from src.schemas.match import MatchCreate, MatchClose, MatchResponse
from src.services.match_service import create_match, close_match

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=MatchResponse, status_code=201)
async def open_match(body: MatchCreate, db: Session = Depends(get_db)):
    return await create_match(body, db)


@router.patch("/{match_id}/close", response_model=MatchResponse)
async def end_match(match_id: str, body: MatchClose, db: Session = Depends(get_db)):
    match = db.query(Match).filter_by(id=match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    if match.status == "finished":
        raise HTTPException(status_code=409, detail="Partie déjà terminée")
    return await close_match(match_id, body, db)


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter_by(id=match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    return match