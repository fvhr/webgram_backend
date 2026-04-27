from dataclasses import dataclass

from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.exceptions import NotFoundError
from src.application.user.dtos.user import OutboundUserDTO


@dataclass
class SetUserUseCase:
    _agent_repository: AgentRepositoryProtocol

    async def __call__(self, agent_uuid: str, user_dto: OutboundUserDTO) -> None:
        if user_dto.agent:
            unset_agent_uuid = str(user_dto.agent.agent_uuid)
            await self._agent_repository.unset_user(unset_agent_uuid)
        _agent_uuid = await self._agent_repository.set_user(agent_uuid, user_dto.user_uuid)
        if not _agent_uuid:
            raise NotFoundError(f'Agent with "{agent_uuid}" not found')
