from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets

from src.application.common.service.send_call_count_event_service import SendCallCountService
from src.application.common.service.send_system_events_service import SendSystemEventsService
from src.domain.enums import WebsocketRoles
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager

dashboard_ws_router = APIRouter(tags=['DashboardWebSocket'])


@dashboard_ws_router.websocket('/backend/dashboard')
@inject
async def dashboard_websocket_endpoint(websocket: WebSocket, connection_manager: FromDishka[ConnectionManager],
                                       send_system_events_service: FromDishka[SendSystemEventsService],
                                       send_call_counts_service: FromDishka[SendCallCountService]):
    personal_uuid = await connection_manager.connect(websocket, WebsocketRoles.DASHBOARD)
    try:
        await send_system_events_service()
        await send_call_counts_service()
        while True:
            await websocket.receive_json()
    except (
            WebSocketDisconnect,
            websockets.exceptions.ConnectionClosed,
            RuntimeError,
    ):
        await connection_manager.disconnect(personal_uuid)
