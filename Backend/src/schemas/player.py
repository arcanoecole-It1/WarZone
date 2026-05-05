from pydantic import BaseModel, UUID4
from datetime import datetime

class PlayerCreate(BaseModel):
    roblox_id: str
    username:  str

class PlayerResponse(BaseModel):
    id:         UUID4
    roblox_id:  str
    username:   str
    win_rate:   float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }