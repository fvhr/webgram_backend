from dataclasses import dataclass

from src.application.common.event_handler import EventHandler
from src.application.domain.event_handlers.heartbeat import DomainHeartbeatEventHandler


@dataclass
class CollectHandlersService:
    _domain_heartbeat_handler: DomainHeartbeatEventHandler

    @property
    def get_handlers(self) -> list[EventHandler]:
        return [self._domain_heartbeat_handler]
