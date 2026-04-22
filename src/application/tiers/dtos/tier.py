from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO
from src.application.queues.dtos.queue import ViewQueueDTO


@dataclass(frozen=True)
class ViewTierDTO(DTO):
    tier_uuid: UUID
    queue: ViewQueueDTO
