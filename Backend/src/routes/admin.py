from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import bcrypt, hashlib
from src.database import get_db
from src.models.admin import Admin, RefreshToken
from src.schemas.admin import AdminLogin, TokenPair, RefreshRequest
from src.auth.jwt import create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenPair)
def login(body: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username=body.username).first()
    if not admin or not bcrypt.checkpw(
        body.password.encode(), admin.password_hash.encode()
    ):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    access_token  = create_access_token(str(admin.id))
    refresh_token = create_refresh_token(str(admin.id))

    # On stocke le hash du refresh token, jamais le token brut
    db.add(RefreshToken(
        admin_id   = admin.id,
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest(),
        expires_at = datetime.now(timezone.utc) + timedelta(days=7),
    ))
    db.commit()
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Mauvais type de token")

    token_hash = hashlib.sha256(body.refresh_token.encode()).hexdigest()
    stored = db.query(RefreshToken).filter_by(
        admin_id=payload["sub"], token_hash=token_hash, revoked=False
    ).first()
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token invalide ou expiré")

    expires_at = stored.expires_at
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        now = now.replace(tzinfo=None)
    if expires_at < now:
        raise HTTPException(status_code=401, detail="Refresh token invalide ou expiré")

    stored.revoked = True
    new_access  = create_access_token(payload["sub"])
    new_refresh = create_refresh_token(payload["sub"])
    db.add(RefreshToken(
        admin_id   = payload["sub"],
        token_hash = hashlib.sha256(new_refresh.encode()).hexdigest(),
        expires_at = datetime.now(timezone.utc) + timedelta(days=7),
    ))
    db.commit()
    return TokenPair(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout", status_code=204)
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(body.refresh_token.encode()).hexdigest()
    stored = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    if stored:
        stored.revoked = True
        db.commit()