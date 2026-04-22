from dataclasses import dataclass
from typing import final

from src.application.queues.dtos.queue import QueueAtcDTO, QueueDTO
from src.application.queues.ports.mappers import QueueDtoEntityMapperProtocol
from src.domain.queues.entities.queue import Queue


@final
@dataclass(frozen=True, slots=True)
class QueueDTOMapper(QueueDtoEntityMapperProtocol):

    def to_entity(self, dto: QueueAtcDTO) -> Queue:
        return Queue(
            queue_uuid=dto.queue_uuid,
            queue_name=dto.queue_name,
            queue_number=dto.queue_number,
            domain_uuid=dto.domain_uuid
        )

    def to_dto(self, entity: Queue) -> QueueDTO:
        return QueueDTO(
            queue_uuid=entity.queue_uuid,
            queue_name=entity.queue_name,
        )
