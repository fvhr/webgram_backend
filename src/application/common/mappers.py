from dataclasses import dataclass
from typing import final

from src.application.common.dtos.event import EventDTO
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol
from src.domain.events.entities.custom_event import CustomEvent


@final
@dataclass(frozen=True, slots=True)
class EventDTOMapper(EventDtoEntityMapperProtocol):

    def to_entity_custom(self, dto: EventDTO) -> CustomEvent:
        return CustomEvent(
            event_name=dto.headers.get('Event-Name'),
            event_action=dto.headers.get('CC-Action'),
            event_agent_uuid=dto.headers.get('CC-Agent'),
            event_agent_status=dto.headers.get('CC-Agent-Status')
        )
