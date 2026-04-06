from abc import abstractmethod
from typing import Protocol

from src.application.queues.dtos.queue import QueueAtcDTO
from src.domain.queues.entities.queue import Queue


class QueueDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: QueueAtcDTO) -> Queue:
        ...
