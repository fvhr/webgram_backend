from dataclasses import dataclass

from src.application.common.ports.external import WebSocketManagerProtocol
from src.domain.enums import WebsocketMessageTypes, WebsocketConnectionTypes
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager


@dataclass
class WebSocketManager(WebSocketManagerProtocol):
    _connection_manager: ConnectionManager

    async def broadcast_message(self, type_message: WebsocketMessageTypes, data: dict,
                                connection_type: WebsocketConnectionTypes) -> None:
        await self._connection_manager.broadcast({'type': type_message, 'data': data}, connection_type)
