from dataclasses import dataclass
from typing import final

from src.domain.queues.entities.queue import Queue
from src.infrastructure.db.models.queues import QueueModel


@final
@dataclass(frozen=True, slots=True)
class QueueDBMapper:
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

    @staticmethod
    def update_model_from_entity(model: QueueModel, entity: Queue) -> None:
        model.queue_number = entity.queue_number
        model.queue_name = entity.queue_name
        model.domain_uuid = entity.domain_uuid
