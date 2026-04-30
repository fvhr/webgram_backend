from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets

from src.domain.enums import WebsocketRoles
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager

dashboard_ws_router = APIRouter(tags=['DashboardWebSocket'])


@dashboard_ws_router.websocket('/backend/dashboard')
@inject
async def dashboard_websocket_endpoint(websocket: WebSocket, connection_manager: FromDishka[ConnectionManager]):
    personal_uuid = await connection_manager.connect(websocket, WebsocketRoles.DASHBOARD)
    try:
        while True:
            await websocket.receive_json()
    except (
            WebSocketDisconnect,
            websockets.exceptions.ConnectionClosed,
            RuntimeError,
    ):
        await connection_manager.disconnect(personal_uuid)
