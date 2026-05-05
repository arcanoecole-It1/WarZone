from pydantic import BaseModel, UUID4
from datetime import datetime

class StatsResponse(BaseModel):
    player_id:    UUID4
    kill_totals:  int
    total_deaths: int
    kd_ratio:     float
    total_wins:   int
    total_matches:int

    model_config = {
        "from_attributes": True
    }

class GradeResponse(BaseModel):
    player_id:  UUID4
    label:      str
    level:      int
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }