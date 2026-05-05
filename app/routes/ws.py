from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request

router = APIRouter()

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    manager = websocket.app.state.ws_manager
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
