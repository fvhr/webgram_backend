from dataclasses import dataclass

from src.application.common.ports.external import WebSocketManagerProtocol
from src.application.common.service.get_calls_service import GetCallsService
from src.domain.enums import WebsocketMessageTypes


@dataclass
class UpgradeSocketUseCase:
    _get_calls_service: GetCallsService
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self, agent_uuid: str) -> None:
        is_change = await self._ws_manager.upgrade_agent_socket(agent_uuid)
        if is_change:
            ws_response = await self._get_calls_service.get_calls()
            await self._ws_manager.personal_to_agent(WebsocketMessageTypes.CONNECT_CALLS, ws_response, agent_uuid)
