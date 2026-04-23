from dataclasses import dataclass

from src.application.common.exceptions import FSAPIError, NotFoundError
from src.application.common.ports.external import FreeswitchAPIProtocol
from src.application.domain.ports.repository import DomainRepositoryProtocol


@dataclass
class SpyAgentUseCase:
    _fsapi: FreeswitchAPIProtocol
    _domain_repository: DomainRepositoryProtocol

    async def __call__(self, call_uuid: str, victim_agent_number: str, spy_agent_number: str, domin_uuid: str) -> None:
        domain_name = await self._domain_repository.get_domain_name_by_domain_uuid(domin_uuid)
        if not domain_name:
            raise NotFoundError(f'Domain {domin_uuid} not found')
        res = await self._fsapi.send_command('originate',
                                             '{'
                                             + f'origination_caller_id_number={victim_agent_number},'
                                             + '}'
                                             + f'user/{spy_agent_number}@{domain_name} '
                                             + f'&eavesdrop({call_uuid})', )
        if not res:
            raise FSAPIError(f'Не удалось подключиться к вызову "{call_uuid}"')
