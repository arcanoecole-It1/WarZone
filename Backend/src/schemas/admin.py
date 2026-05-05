from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class TokenPair(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str