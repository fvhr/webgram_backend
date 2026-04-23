from dataclasses import dataclass

from src.application.common.exceptions import FSAPIError
from src.application.common.ports.external import FreeswitchAPIProtocol


@dataclass
class SetStatusUseCase:
    _fsapi: FreeswitchAPIProtocol

    async def __call__(self, agent_uuid: str, new_status: str) -> None:
        res = await self._fsapi.send_command('callcenter_config',
                                             f"agent set status {agent_uuid} '{new_status}'")
        if not res:
            raise FSAPIError(f'Не удалось поменять статус агенту "{agent_uuid}": {res}')
