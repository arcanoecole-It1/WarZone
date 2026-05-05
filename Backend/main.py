from fastapi import FastAPI
import bcrypt

from src.routes import players , matches , kills , admin , analytics , leaderboard
from src.database import engine, Base, SessionLocal
from src.models.admin import Admin
from src.config import settings

Base.metadata.create_all(bind=engine)

def create_default_admin() -> None:
    db = SessionLocal()
    try:
        existing_admin = db.query(Admin).first()
        if existing_admin is None:
            default_username = settings.DEFAULT_ADMIN_USERNAME
            default_password = settings.DEFAULT_ADMIN_PASSWORD
            password_hash = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()
            db.add(Admin(username=default_username, password_hash=password_hash))
            db.commit()
    finally:
        db.close()

create_default_admin()

app = FastAPI(title="Warzone API", description="API pour gérer les joueurs, les matchs et les statistiques de Warzone")

app.include_router(players.router)
app.include_router(matches.router)
app.include_router(kills.router)
app.include_router(leaderboard.router)
app.include_router(analytics.router)
app.include_router(admin.router)

