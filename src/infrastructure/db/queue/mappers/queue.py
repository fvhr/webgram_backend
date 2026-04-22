from dataclasses import dataclass
from typing import final

from src.application.queues.dtos.queue import ViewQueueDTO, QueueDTO
from src.domain.queues.entities.queue import Queue
from src.infrastructure.db.domain.mappers.domain import DomainDBMapper
from src.infrastructure.db.models.queues import QueueModel


@final
@dataclass(frozen=True, slots=True)
class QueueDBMapper:
    _domain_db_mapper: DomainDBMapper

    @staticmethod
    def to_entity(model: QueueModel) -> Queue:
        return Queue(
            queue_uuid=model.queue_uuid,
            queue_name=model.queue_name,
            queue_number=model.queue_number,
            domain_uuid=model.domain_uuid,
        )

    @staticmethod
    def to_model(entity: Queue) -> QueueModel:
        return QueueModel(
            queue_uuid=entity.queue_uuid,
            queue_name=entity.queue_name,
            queue_number=entity.queue_number,
            domain_uuid=entity.domain_uuid,
        )

    def to_view_dto(self, entity: QueueModel) -> ViewQueueDTO:
        domain_dto = self._domain_db_mapper.to_dto(entity.domain)
        return ViewQueueDTO(
            queue_uuid=entity.queue_uuid,
            queue_number=entity.queue_number,
            domain=domain_dto,
        )

    @staticmethod
    def to_dto(entity: QueueModel) -> QueueDTO:
        return QueueDTO(
            queue_uuid=entity.queue_uuid,
            queue_name=entity.queue_name,
        )

    @staticmethod
    def update_model_from_entity(model: QueueModel, entity: Queue) -> None:
        model.queue_number = entity.queue_number
        model.queue_name = entity.queue_name
        model.domain_uuid = entity.domain_uuid
