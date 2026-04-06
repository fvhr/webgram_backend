from abc import abstractmethod
from typing import Protocol

from src.domain.queues.entities.queue import Queue


class QueueRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_or_update_queue(self, queue: Queue) -> Queue:
        raise NotImplementedError

    @abstractmethod
    async def delete_queue(self, queue_uuid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_queues(self) -> list[Queue]:
        raise NotImplementedError
