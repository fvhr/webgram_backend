import asyncio
from dataclasses import dataclass

from genesis import Inbound, ESLEvent

from src.application.common.service.collect_handlers_service import CollectHandlersService
from src.settings import Settings


async def handle_event(event: ESLEvent):
    print('dsadasdasdasdasda')


async def handle_event2(event: ESLEvent):
    print(dir(event))
    print(event)
    print('dsadasdasda22222222222222sdasda')


@dataclass
class FreeSwitchEventListen:
    settings: Settings
    collect_handlers_service: CollectHandlersService
    reconnect_count: int = 10

    async def __call__(self):
        while self.reconnect_count != 0:
            async with Inbound(self.settings.FS_HOST, int(self.settings.FS_PORT), self.settings.FS_PASSWORD) as client:
                for handler in self.collect_handlers_service.get_handlers:
                    client.on(handler.get_event_name, handler)
                    await client.send(f'EVENTS PLAIN {handler.get_event_name}')
                while client.is_connected:
                    await asyncio.sleep(1)
            self.reconnect_count -= 1
        exit(0)
