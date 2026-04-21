from dataclasses import dataclass
from uuid import UUID

from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.exceptions import NotFoundError


@dataclass
class SetUserUseCase:
    _agent_repository: AgentRepositoryProtocol

    async def __call__(self, agent_uuid: str, user_uuid: UUID) -> None:
        _agent_uuid = await self._agent_repository.set_user(agent_uuid, user_uuid)
        if not _agent_uuid:
            raise NotFoundError(f'Agent with "{agent_uuid}" not found')
