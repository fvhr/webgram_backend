from dataclasses import dataclass

from src.application.agents.dtos.agent import AgentFreeDTO
from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.application.agents.ports.repository import AgentRepositoryProtocol


@dataclass
class GetFreeAgentsUseCase:
    _agent_repository: AgentRepositoryProtocol
    _agent_mapper: AgentDtoEntityMapperProtocol

    async def __call__(self) -> list[AgentFreeDTO]:
        agents = await self._agent_repository.get_free_agents()
        return [self._agent_mapper.to_free_dto(entity) for entity in agents]
