import asyncio
import json
import aiomqtt
from app.config import settings
from app.ml.inference import run_inference
from app.db.influx import write_reading

async def start_mqtt_listener(app):
    asyncio.create_task(_listen(app))

async def _listen(app):
    async with aiomqtt.Client(
        hostname=settings.MQTT_BROKER,
        port=settings.MQTT_PORT,
    ) as client:
        await client.subscribe(settings.MQTT_TOPIC_SENSORS)
        print(f"[MQTT] Subscribed to {settings.MQTT_TOPIC_SENSORS}")
        async with client.messages() as messages:
            async for message in messages:
                try:
                    payload = json.loads(message.payload.decode())
                    device_id = payload.get("d", "unknown")
                    flow      = float(payload.get("f", 0))
                    pressure  = float(payload.get("p", 0))
                    result = run_inference(app.state.model, device_id, flow, pressure)
                    write_reading(
                        app.state.influx,
                        device_id=device_id,
                        user_id="system",
                        role="home",
                        flow=flow,
                        pressure=pressure,
                        is_anomaly=result["is_anomaly"],
                        score=result["score"],
                    )
                    if result["is_anomaly"]:
                        await app.state.ws_manager.broadcast({
                            "type": "anomaly",
                            "device_id": device_id,
                            "flow": flow,
                            "pressure": pressure,
                            "score": result["score"],
                        })
                        print(f"[MQTT] Anomaly on {device_id} score={result['score']}")
                except Exception as e:
                    print(f"[MQTT] Error: {e}")
