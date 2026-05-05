from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    device_id: str
    flow: float
    pressure: float
    timestamp: datetime

class SensorPayload(BaseModel):
    d: str
    f: float
    p: float
    t: int
