from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets

from src.presentation.api.v1.websocket.connection_manager import ConnectionManager

ws_router = APIRouter(tags=['WebSocket'])


@ws_router.websocket('/')
@inject
async def websocket_endpoint(websocket: WebSocket, connection_manager: FromDishka[ConnectionManager]):
    personal_uuid = await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_json()
    except (
            WebSocketDisconnect,
            websockets.exceptions.ConnectionClosed,
            RuntimeError,
    ):
        await connection_manager.disconnect(personal_uuid)
