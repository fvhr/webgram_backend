from dataclasses import dataclass

from src.application.common.ports.external import WebSocketManagerProtocol, \
    FreeswitchAPIProtocol
from src.domain.enums import WebsocketMessageTypes, WebsocketRoles


@dataclass
class SendCallCountService:
    _fsapi: FreeswitchAPIProtocol
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self) -> None:
        count = await self._fsapi.get_calls_count()
        await self._ws_manager.broadcast_message_to_role(WebsocketMessageTypes.CALL_COUNT,
                                                 {'calls_count': count},
                                                 WebsocketRoles.DASHBOARD)
