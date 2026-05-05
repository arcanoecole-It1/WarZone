from pydantic import BaseModel , UUID4
from datetime import datetime

class KillCreate(BaseModel):
    killer_id: UUID4
    victim_id: UUID4
    match_id: UUID4
    weapon: str
    timestamp: datetime

class KillResponse(BaseModel):
    id: UUID4
    match_id: UUID4
    killer_id: UUID4
    victim_id: UUID4
    weapon: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    } 