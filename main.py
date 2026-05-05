from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, sensors, valve, history, ws
from app.services.mqtt import start_mqtt_listener
from app.services.decision import start_decision_loop
from app.services.websocket import ConnectionManager
from app.ml.loader import load_model
from app.db.influx import get_influx_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.influx     = get_influx_client()
    app.state.model      = load_model()
    app.state.ws_manager = ConnectionManager()
    await start_mqtt_listener(app)
    await start_decision_loop(app)
    yield
    app.state.influx.close()

app = FastAPI(title="AquaShield API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/auth",    tags=["auth"])
app.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
app.include_router(valve.router,   prefix="/valve",   tags=["valve"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(ws.router,      prefix="/ws",      tags=["websocket"])

@app.get("/health")
async def health():
    return {"status": "ok", "project": "AquaShield"}
