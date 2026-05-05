from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.admin import Admin
from src.config import settings

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(admin_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=15)
    return jwt.encode(
        {"sub": admin_id, "exp": exp, "type": "access"},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

def create_refresh_token(admin_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    return jwt.encode(
        {"sub": admin_id, "exp": exp, "type": "refresh"},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

def get_current_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    db:    Annotated[Session, Depends(get_db)],
) -> Admin:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Mauvais type de token")
    admin = db.query(Admin).filter_by(id=payload["sub"]).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin introuvable")
    return admin

CurrentAdmin = Annotated[Admin, Depends(get_current_admin)]