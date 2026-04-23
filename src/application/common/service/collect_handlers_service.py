from dataclasses import dataclass

from src.application.agents.event_handlers.channel_create import ChannelCreateEventHandler
from src.application.agents.event_handlers.status_change import AgentStatusChangeEventHandler
from src.application.common.event_handler import EventHandler
from src.application.domain.event_handlers.heartbeat import DomainHeartbeatEventHandler
from src.application.extensions.event_handlers.heartbeat import ExtensionHeartbeatEventHandler
from src.application.queues.event_handlers.heartbeat import QueueHeartbeatEventHandler


@dataclass
class CollectHandlersService:
    _domain_heartbeat_handler: DomainHeartbeatEventHandler
    _extension_heartbeat_handler: ExtensionHeartbeatEventHandler
    _queue_heartbeat_handler: QueueHeartbeatEventHandler
    _agent_status_change_handler: AgentStatusChangeEventHandler
    _agent_channel_create_handler: ChannelCreateEventHandler

    @property
    def get_handlers(self) -> list[EventHandler]:
        return [self._domain_heartbeat_handler, self._extension_heartbeat_handler, self._queue_heartbeat_handler,
                self._agent_status_change_handler, self._agent_channel_create_handler]
