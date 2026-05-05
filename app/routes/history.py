from fastapi import APIRouter, Depends, Request
from app.deps import get_current_user, get_influx
from app.config import settings
from app.models.user import TokenData

router = APIRouter()

@router.get("/")
async def get_history(
    device_id: str,
    hours: int = 1,
    user: TokenData = Depends(get_current_user),
    influx = Depends(get_influx),
):
    query = f'''
    from(bucket: "{settings.INFLUX_BUCKET}")
      |> range(start: -{hours}h)
      |> filter(fn: (r) => r["device_id"] == "{device_id}")
      |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
    '''
    query_api = influx.query_api()
    tables = query_api.query(query)
    results = []
    for table in tables:
        for record in table.records:
            results.append({
                "time": str(record.get_time()),
                "field": record.get_field(),
                "value": record.get_value(),
            })
    return results
