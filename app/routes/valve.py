from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.models.user import TokenData

router = APIRouter()

valve_state = {"open": True}

@router.get("/state")
async def get_state(user: TokenData = Depends(get_current_user)):
    return valve_state

@router.post("/open")
async def open_valve(user: TokenData = Depends(get_current_user)):
    valve_state["open"] = True
    return {"status": "opened"}

@router.post("/close")
async def close_valve(user: TokenData = Depends(get_current_user)):
    valve_state["open"] = False
    return {"status": "closed"}
