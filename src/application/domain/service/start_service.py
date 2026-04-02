from dataclasses import dataclass

from src.application.common.ports.atc_gateway import AtcGatewayProtocol
from src.application.domain.ports.repository import DomainRepositoryProtocol
from src.logger import logger


@dataclass
class SyncDomainService:
    _domain_repository: DomainRepositoryProtocol
    _atc_gateway: AtcGatewayProtocol

    async def __call__(self) -> None:
        now_domains = await self._domain_repository.get_domains()
        update_domains = await self._atc_gateway.get_atc_domains()
        for entity in update_domains:
            await self._domain_repository.create_or_update_domain(entity)

        delete_uuids_set = set([entity.domain_uuid for entity in now_domains]) - set(
            [entity.domain_uuid for entity in update_domains])

        for _uuid in delete_uuids_set:
            await self._domain_repository.delete_domain(str(_uuid))
        active_domains = [entity.domain_name.value for entity in update_domains if entity.domain_enabled]
        logger.info(f'Активные домены: {active_domains}')
