from dataclasses import dataclass

from genesis import ESLEvent

from src.application.common.event_handler import EventHandler
from src.application.domain.service.sync_service import SyncDomainService
from src.domain.events.entities.base_event import BaseEvent, EventTypes


@dataclass
class DomainHeartbeatEventHandler(EventHandler):
    _domain_sync_service: SyncDomainService
    _heartbeat_count: int = 0

    async def __call__(self, event: ESLEvent):
        self._heartbeat_count += 1
        if self._heartbeat_count == 5:
            await self._domain_sync_service()

    @property
    def get_event_name(self) -> str:
        return EventTypes.HEARTBEAT
