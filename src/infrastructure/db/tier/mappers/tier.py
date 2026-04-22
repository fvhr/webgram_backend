from dataclasses import dataclass
from typing import final

from src.application.tiers.dtos.tier import ViewTierDTO
from src.domain.tiers.entities.tier import Tier
from src.infrastructure.db.models import TierModel
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper


@final
@dataclass(frozen=True, slots=True)
class TierDBMapper:
    _queue_db_mapper: QueueDBMapper

    @staticmethod
    def to_entity(model: TierModel) -> Tier:
        return Tier(
            tier_uuid=model.tier_uuid,
            agent_uuid=model.agent_uuid,
            queue_uuid=model.queue_uuid,
        )

    @staticmethod
    def to_model(entity: Tier) -> TierModel:
        return TierModel(
            tier_uuid=entity.tier_uuid,
            agent_uuid=entity.agent_uuid,
            queue_uuid=entity.queue_uuid,
        )

    def to_dto(self, model: TierModel) -> ViewTierDTO:
        queue_dto = self._queue_db_mapper.to_view_dto(model.queue)
        return ViewTierDTO(
            tier_uuid=model.tier_uuid,
            queue=queue_dto
        )
