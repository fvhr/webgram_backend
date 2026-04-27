from dataclasses import dataclass

from src.application.agents.dtos.agent import AgentHistoryDTO
from src.application.common.ports.external import AtcGatewayProtocol


@dataclass
class GetHistoryAgentByDayUseCase:
    _atc_gateway: AtcGatewayProtocol

    async def __call__(self, agent_number: str) -> list[AgentHistoryDTO]:
        return await self._atc_gateway.get_atc_history_agent_by_day(agent_number)
