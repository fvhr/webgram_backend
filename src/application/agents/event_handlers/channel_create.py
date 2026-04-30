import asyncio
from dataclasses import dataclass

from src.application.common.dtos.event import EventDTO
from src.application.common.event_handler import EventHandler
from src.application.common.ports.external import WebSocketManagerProtocol
from src.application.common.service.get_calls_service import GetCallsService
from src.domain.enums import WebsocketMessageTypes, WebsocketRoles
from src.domain.events.entities.base_event import EventTypes


@dataclass
class ChannelCreateEventHandler(EventHandler):
    _get_calls_service: GetCallsService
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self, event: EventDTO) -> None:
        await asyncio.sleep(0.5)  # в апи появляется позже чем приходит событие
        ws_response = await self._get_calls_service.get_calls()
        await self._ws_manager.broadcast_message_to_role(WebsocketMessageTypes.UPDATE_CALLS, ws_response,
                                                 WebsocketRoles.ADMIN)

    @property
    def get_event_names(self) -> list:
        return [EventTypes.CHANNEL_CREATE, EventTypes.CHANNEL_DESTROY,
                EventTypes.CHANNEL_ANSWER]
