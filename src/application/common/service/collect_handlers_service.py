from dataclasses import dataclass

from src.application.common.event_handler import EventHandler
from src.application.domain.event_handlers.heartbeat import DomainHeartbeatEventHandler
from src.application.extensions.event_handlers.heartbeat import ExtensionHeartbeatEventHandler
from src.application.queues.event_handlers.heartbeat import QueueHeartbeatEventHandler


@dataclass
class CollectHandlersService:
    _domain_heartbeat_handler: DomainHeartbeatEventHandler
    _extension_heartbeat_handler: ExtensionHeartbeatEventHandler
    _queue_heartbeat_handler: QueueHeartbeatEventHandler

    @property
    def get_handlers(self) -> list[EventHandler]:
        return [self._domain_heartbeat_handler, self._extension_heartbeat_handler, self._queue_heartbeat_handler]
