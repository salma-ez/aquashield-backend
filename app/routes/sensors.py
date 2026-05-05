from fastapi import APIRouter, Depends, Request
from app.deps import get_current_user, get_model
from app.ml.inference import run_inference
from app.models.user import TokenData

router = APIRouter()

@router.post("/ingest")
async def ingest(
    request: Request,
    device_id: str,
    flow: float,
    pressure: float,
    user: TokenData = Depends(get_current_user),
    model = Depends(get_model),
):
    result = run_inference(model, device_id, flow, pressure)
    return result
