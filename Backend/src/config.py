from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY:   str
    DEFAULT_ADMIN_USERNAME: str 
    DEFAULT_ADMIN_PASSWORD: str 
    class Config: env_file = ".env"

settings = Settings()