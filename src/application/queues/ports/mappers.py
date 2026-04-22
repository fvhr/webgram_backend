from abc import abstractmethod
from typing import Protocol

from src.application.queues.dtos.queue import QueueAtcDTO, QueueDTO
from src.domain.queues.entities.queue import Queue


class QueueDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: QueueAtcDTO) -> Queue:
        ...

    @abstractmethod
    def to_dto(self, entity: Queue) -> QueueDTO:
        ...
