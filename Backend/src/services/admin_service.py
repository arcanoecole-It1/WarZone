import bcrypt
from src.auth.jwt import jwt
from datetime import timedelta
from src.models.admin import Admin, RefreshToken
from src.schemas.admin import AdminLogin, TokenPair
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.config import SECRET_KEY
from datetime import datetime, timezone

def login(kill: AdminLogin, db: Session) -> TokenPair:
    admin = db.query(Admin).filter_by(username=kill.username).first()
    if not admin or not bcrypt.checkpw(kill.password.encode(), admin.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    access  = _make_token(admin.id, minutes=15)
    refresh = _make_token(admin.id, minutes=60*24*7)
    db.add(RefreshToken(admin_id=admin.id, token_hash=refresh))
    db.commit()
    return TokenPair(access_token=access, refresh_token=refresh)

def _make_token(admin_id, minutes: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode({"sub": str(admin_id), "exp": exp}, SECRET_KEY)