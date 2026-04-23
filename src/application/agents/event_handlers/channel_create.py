import asyncio
from dataclasses import dataclass

from src.application.common.dtos.event import EventDTO
from src.application.common.event_handler import EventHandler
from src.application.common.ports.external import WebSocketManagerProtocol
from src.application.common.service.get_calls_service import GetCallsService
from src.domain.enums import WebsocketMessageTypes
from src.domain.events.entities.base_event import EventTypes


@dataclass
class ChannelCreateEventHandler(EventHandler):
    _get_calls_service: GetCallsService
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self, event: EventDTO) -> None:
        await asyncio.sleep(0.5)  # в апи появляется позже чем приходит событие
        ws_response = await self._get_calls_service.get_calls()
        await self._ws_manager.broadcast_message(WebsocketMessageTypes.UPDATE_CALLS, ws_response)

    @property
    def get_event_names(self) -> list:
        return [EventTypes.CHANNEL_CREATE, EventTypes.CHANNEL_DESTROY,
                EventTypes.CHANNEL_ANSWER]
