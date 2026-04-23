from dataclasses import dataclass

from src.application.common.dtos.event import EventDTO
from src.application.common.event_handler import EventHandler
from src.application.domain.service.sync_service import SyncDomainService
from src.application.extensions.service.sync_extension import SyncExtensionService
from src.domain.events.entities.base_event import EventTypes


@dataclass
class ExtensionHeartbeatEventHandler(EventHandler):
    _extension_sync_service: SyncExtensionService
    _heartbeat_count: int = 0

    async def __call__(self, event: EventDTO):
        self._heartbeat_count += 1
        if self._heartbeat_count == 5:
            await self._extension_sync_service()

    @property
    def get_event_names(self) -> list:
        return [EventTypes.HEARTBEAT]
