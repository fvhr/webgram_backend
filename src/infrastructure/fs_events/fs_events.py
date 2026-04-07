import asyncio
from dataclasses import dataclass

from genesis import Inbound, ESLEvent

from src.application.common.event_handler import EventHandler
from src.application.common.service.collect_handlers_service import CollectHandlersService
from src.infrastructure.fs_events.mappers import EventMapper
from src.logger import logger
from src.settings import Settings


@dataclass
class FreeSwitchEventListen:
    settings: Settings
    collect_handlers_service: CollectHandlersService
    mapper: EventMapper
    reconnect_count: int = 10

    async def __call__(self):
        while self.reconnect_count != 0:
            async with Inbound(self.settings.FS_HOST, int(self.settings.FS_PORT), self.settings.FS_PASSWORD) as client:
                unique_events = set([handler.get_event_name for handler in self.collect_handlers_service.get_handlers])
                for event_name in unique_events:
                    client.on(event_name, self.mapping_event)
                    await client.send(f'EVENTS PLAIN {event_name}')
                while client.is_connected:
                    await asyncio.sleep(1)
            self.reconnect_count -= 1
        exit(0)

    async def mapping_event(self, event: ESLEvent):
        event_dto = self.mapper.to_dto(event)
        event_name = event_dto.headers.get('Event-Name')
        logger.debug(f'Получено событие: {event_name}')
        if event_name in self.get_handlers:
            handlers = self.get_handlers.get(event_name)
            for handler in handlers:
                await handler(event_dto)

    @property
    def get_handlers(self) -> dict[str, list[EventHandler]]:
        handlers = {}
        for handler in self.collect_handlers_service.get_handlers:
            if handler.get_event_name not in handlers:
                handlers[handler.get_event_name] = [handler]
            else:
                handlers[handler.get_event_name].append(handler)
        return handlers
