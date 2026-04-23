from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets

from src.application.common.service.get_calls_service import GetCallsService
from src.domain.enums import WebsocketMessageTypes
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager

ws_router = APIRouter(tags=['WebSocket'])


@ws_router.websocket('/')
@inject
async def websocket_endpoint(websocket: WebSocket, connection_manager: FromDishka[ConnectionManager],
                             get_calls_service: FromDishka[GetCallsService]):
    personal_uuid = await connection_manager.connect(websocket)
    try:
        ws_response = await get_calls_service.get_calls()
        await websocket.send_json({'type': WebsocketMessageTypes.CONNECT_CALLS, 'data': ws_response})
        while True:
            await websocket.receive_json()
    except (
            WebSocketDisconnect,
            websockets.exceptions.ConnectionClosed,
            RuntimeError,
    ):
        await connection_manager.disconnect(personal_uuid)
