from pydantic import BaseModel

class OverviewResponse(BaseModel):
    total_kills:   int
    total_matches: int
    active_players:int

    model_config = {
        "from_attributes": True
    }
class WeaponStat(BaseModel):
    weapon: str
    count:  int

class DailyStat(BaseModel):
    date:    str
    matches: int