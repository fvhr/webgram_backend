from dataclasses import dataclass

from src.application.agents.dtos.agent import AgentHistoryDTO
from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.exceptions import NotFoundError
from src.application.common.ports.external import AtcGatewayProtocol


@dataclass
class GetHistoryAgentByDayUseCase:
    _atc_gateway: AtcGatewayProtocol
    _agent_repository: AgentRepositoryProtocol

    async def __call__(self, agent_number: str) -> list[AgentHistoryDTO]:
        agent_uuid = await self._agent_repository.get_agent_uuid_by_agent_num(agent_number)
        if not agent_uuid:
            raise NotFoundError(f'Agent {agent_number} not found')
        return await self._atc_gateway.get_atc_history_agent_by_day(agent_number, str(agent_uuid))
