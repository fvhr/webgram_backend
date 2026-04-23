from dataclasses import dataclass

from src.application.common.dtos.event import EventDTO
from src.application.common.event_handler import EventHandler
from src.application.domain.service.sync_service import SyncDomainService
from src.application.extensions.service.sync_extension import SyncExtensionService
from src.application.queues.service.sync_queue_service import SyncQueueService
from src.domain.events.entities.base_event import EventTypes


@dataclass
class QueueHeartbeatEventHandler(EventHandler):
    _queue_sync_service: SyncQueueService
    _heartbeat_count: int = 0

    async def __call__(self, event: EventDTO):
        self._heartbeat_count += 1
        if self._heartbeat_count == 5:
            await self._queue_sync_service()

    @property
    def get_event_names(self) -> list:
        return [EventTypes.HEARTBEAT]
