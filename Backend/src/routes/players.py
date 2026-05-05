from fastapi import APIRouter, Depends, HTTPException , Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.player import PlayerCreate, PlayerResponse
from src.services.player_service import register_player

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerResponse, status_code=201)
async def create_player(body: PlayerCreate, db: Session = Depends(get_db), content_type: str = Header(None)):
    if content_type is None or "application/json" not in content_type.lower():
        raise HTTPException(status_code=415, detail="Content-Type doit être application/json")
    # Évite les doublons si Roblox appelle plusieurs fois
    existing = db.query(User).filter_by(roblox_id=body.roblox_id).first()
    if existing:
        return existing
    return await register_player(body, db)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str, db: Session = Depends(get_db)):
    player = db.query(User).filter_by(id=player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Joueur introuvable")
    return player
