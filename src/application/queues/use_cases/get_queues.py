from dataclasses import dataclass

from src.application.queues.dtos.queue import QueueDTO
from src.application.queues.ports.mappers import QueueDtoEntityMapperProtocol
from src.application.queues.ports.repository import QueueRepositoryProtocol


@dataclass
class GetQueuesUseCase:
    _queue_repository: QueueRepositoryProtocol
    _queue_mapper: QueueDtoEntityMapperProtocol

    async def __call__(self) -> list[QueueDTO]:
        queues_entities = await self._queue_repository.get_queues()
        return [self._queue_mapper.to_dto(entity) for entity in queues_entities]
