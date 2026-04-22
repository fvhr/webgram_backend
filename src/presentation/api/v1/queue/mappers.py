from dataclasses import dataclass
from typing import final

from src.application.queues.dtos.queue import QueueDTO
from src.presentation.api.v1.queue.schemas.responses import QueueResponseSchema


@final
@dataclass(frozen=True, slots=True)
class QueuePresentationMapper:
    @staticmethod
    def to_response(dto: QueueDTO) -> QueueResponseSchema:
        """Convert Application DTO to API Response model."""
        return QueueResponseSchema(
            queue_uuid=dto.queue_uuid,
            queue_name=dto.queue_name,
        )
