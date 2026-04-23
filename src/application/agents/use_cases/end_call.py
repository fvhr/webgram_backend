from dataclasses import dataclass

from src.application.common.exceptions import FSAPIError
from src.application.common.ports.external import FreeswitchAPIProtocol


@dataclass
class EndCallUseCase:
    _fsapi: FreeswitchAPIProtocol

    async def __call__(self, call_uuid: str) -> None:
        res = await self._fsapi.send_command('uuid_kill', call_uuid)
        if not res:
            raise FSAPIError(f'Не удалось сбросить вызов "{call_uuid}"')
