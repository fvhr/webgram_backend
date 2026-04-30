from dataclasses import dataclass

from src.application.common.ports.external import WebSocketManagerProtocol
from src.domain.enums import WebsocketMessageTypes, WebsocketRoles
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager


@dataclass
class WebSocketManager(WebSocketManagerProtocol):
    _connection_manager: ConnectionManager

    async def broadcast_message_to_role(self, type_message: WebsocketMessageTypes, data: dict,
                                        ws_role: WebsocketRoles) -> None:
        await self._connection_manager.broadcast_to_role({'type': type_message, 'data': data}, ws_role)

    async def upgrade_agent_socket(self, agent_uuid: str) -> bool:
        return await self._connection_manager.upgrade_agent_socket(agent_uuid)

    async def personal_to_agent(self, type_message: WebsocketMessageTypes, data: dict, agent_uuid: str) -> None:
        await self._connection_manager.personal_to_agent({'type': type_message, 'data': data}, agent_uuid)
