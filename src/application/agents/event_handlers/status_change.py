from dataclasses import dataclass

from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.dtos.event import EventDTO
from src.application.common.event_handler import EventHandler
from src.application.common.ports.external import WebSocketManagerProtocol
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol
from src.domain.enums import WebsocketMessageTypes, WebsocketConnectionTypes
from src.domain.events.entities.base_event import EventTypes


@dataclass
class AgentStatusChangeEventHandler(EventHandler):
    _agent_repository: AgentRepositoryProtocol
    _agent_mapper: AgentDtoEntityMapperProtocol
    _event_mapper: EventDtoEntityMapperProtocol
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self, event: EventDTO):
        custom_event = self._event_mapper.to_entity_custom(event)
        if custom_event.event_action == 'agent-status-change':
            if custom_event.event_agent_status and custom_event.event_agent_uuid:
                agent = await self._agent_repository.change_status_agent(custom_event.event_agent_uuid,
                                                                         custom_event.event_agent_status)
                agent_dict = self._agent_mapper.to_dict(agent)
                await self._ws_manager.broadcast_message(WebsocketMessageTypes.AGENT_DATA, agent_dict,
                                                         WebsocketConnectionTypes.OPERATOR_PANEL)

    @property
    def get_event_names(self) -> list:
        return [EventTypes.CUSTOM]
