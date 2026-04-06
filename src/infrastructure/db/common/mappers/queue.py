from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.application.queues.dtos.queue import QueueAtcDTO


@final
@dataclass(frozen=True, slots=True)
class QueueGatewayDBMapper:
    @staticmethod
    def to_entity(model: Row) -> QueueAtcDTO:
        return QueueAtcDTO(
            queue_uuid=model.call_center_queue_uuid,
            queue_number=model.queue_extension,
            queue_name=model.queue_name,
            domain_uuid=model.domain_uuid,
        )
