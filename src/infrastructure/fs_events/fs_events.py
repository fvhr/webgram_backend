from dataclasses import dataclass

from src.settings import Settings


@dataclass
class FreeSwitchEventListen:
    settings: Settings
    reconnect_count: int = 10

    async def __call__(self):
        ...
