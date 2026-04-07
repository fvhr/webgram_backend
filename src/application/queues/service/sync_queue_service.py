from dataclasses import dataclass

from src.application.common.ports.external import AtcGatewayProtocol
from src.application.queues.ports.mappers import QueueDtoEntityMapperProtocol
from src.application.queues.ports.repository import QueueRepositoryProtocol
from src.logger import logger


@dataclass
class SyncQueueService:
    _queue_repository: QueueRepositoryProtocol
    _atc_gateway: AtcGatewayProtocol
    _queue_mapper: QueueDtoEntityMapperProtocol

    async def __call__(self) -> None:
        now_queues = await self._queue_repository.get_queues()
        update_queues = await self._atc_gateway.get_atc_queues()
        for dto in update_queues:
            entity = self._queue_mapper.to_entity(dto)
            await self._queue_repository.create_or_update_queue(entity)

        delete_uuids_set = set([entity.queue_uuid for entity in now_queues]) - set(
            [dto.queue_uuid for dto in update_queues])

        for _uuid in delete_uuids_set:
            await self._queue_repository.delete_queue(str(_uuid))
        logger.info(f'Очереди в системе: {[queue.queue_name for queue in update_queues]}')
