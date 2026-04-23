import uuid
from dataclasses import dataclass

from src.application.agents.dtos.agent import AgentDTO
from src.application.agents.ports.repository import ViewAgentRepositoryProtocol
from src.application.common.exceptions import NotFoundError
from src.application.common.ports.external import FreeswitchAPIProtocol
from src.application.queues.ports.repository import ViewQueueRepositoryProtocol
from src.application.tiers.ports.repository import TierRepositoryProtocol, ViewTierRepositoryProtocol
from src.domain.tiers.entities.tier import Tier


@dataclass
class SetQueuesUseCase:
    _view_tier_repository: ViewTierRepositoryProtocol
    _tier_repository: TierRepositoryProtocol
    _queue_view_repository: ViewQueueRepositoryProtocol
    _agent_view_repository: ViewAgentRepositoryProtocol
    _fsapi: FreeswitchAPIProtocol

    async def __call__(self, agent_uuid: str, queue_uuids: list[str]) -> AgentDTO:
        agent_tiers = await self._view_tier_repository.get_agent_tiers(agent_uuid)
        now_queue_uuids = set([str(tier.queue.queue_uuid) for tier in agent_tiers])
        for queue_uuid in set(queue_uuids):
            if queue_uuid not in now_queue_uuids:
                queue_dto = await self._queue_view_repository.get_queue(queue_uuid)
                if queue_dto:
                    queue_id = f'{queue_dto.queue_number}@{queue_dto.domain.domain_name}'
                    res = await self._fsapi.send_command('callcenter_config',
                                                         f'tier add {queue_id} {agent_uuid} 0 0')
                    if res:
                        tier = Tier(tier_uuid=uuid.uuid4(), agent_uuid=uuid.UUID(agent_uuid),
                                    queue_uuid=uuid.UUID(queue_uuid))
                        await self._tier_repository.create_tier(tier)
        for tier in agent_tiers:
            if str(tier.queue.queue_uuid) not in queue_uuids:
                queue_id = f'{tier.queue.queue_number}@{tier.queue.domain.domain_name}'
                res = await self._fsapi.send_command('callcenter_config',
                                                     f'tier del {queue_id} {agent_uuid}')
                if res:
                    await self._tier_repository.delete_tier(agent_uuid, str(tier.queue.queue_uuid))
        agent_dto = await self._agent_view_repository.get_agent(agent_uuid)
        if not agent_dto:
            raise NotFoundError(
                f'Agent with "{agent_uuid}" not found'
            )
        return agent_dto
