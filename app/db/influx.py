from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config import settings

def get_influx_client() -> InfluxDBClient:
    return InfluxDBClient(
        url=settings.INFLUX_URL,
        token=settings.INFLUX_TOKEN,
        org=settings.INFLUX_ORG,
    )

def write_reading(client, device_id, user_id, role, flow, pressure, is_anomaly, score):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("sensor_reading")
        .tag("device_id", device_id)
        .tag("user_id", user_id)
        .tag("role", role)
        .field("flow", flow)
        .field("pressure", pressure)
        .field("is_anomaly", int(is_anomaly))
        .field("ml_score", score)
    )
    write_api.write(bucket=settings.INFLUX_BUCKET, record=point)
