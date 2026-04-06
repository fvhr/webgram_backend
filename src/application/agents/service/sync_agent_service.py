from dataclasses import dataclass

from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.ports.atc_gateway import AtcGatewayProtocol
from src.logger import logger


@dataclass
class SyncAgentService:
    _agent_repository: AgentRepositoryProtocol
    _atc_gateway: AtcGatewayProtocol
    _agent_mapper: AgentDtoEntityMapperProtocol

    async def __call__(self) -> None:
        now_agents = await self._agent_repository.get_agents()
        update_agents = await self._atc_gateway.get_atc_agents()
        await self._agent_repository.create_or_update_all_agents([self._agent_mapper.to_entity(dto) for dto in update_agents])

        delete_uuids_set = set([entity.agent_uuid for entity in now_agents]) - set(
            [dto.agent_uuid for dto in update_agents])

        for _uuid in delete_uuids_set:
            await self._agent_repository.delete_agent(str(_uuid))
        logger.info(f'Всего агентов в системе: {len(update_agents)}')
