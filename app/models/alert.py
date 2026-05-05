from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional

class Alert(BaseModel):
    device_id: str
    type: Literal["anomaly", "spike", "volume", "time", "manual"]
    message: str
    valve_action: Literal["close", "open", "none"]
    score: Optional[float] = None
    timestamp: datetime
