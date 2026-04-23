from dataclasses import dataclass
from typing import final
from uuid import UUID

from src.application.common.dtos.event import EventDTO
from src.application.common.dtos.fsapi import ShowCallsDTO
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol, FSAPIDtoEntityMapperProtocol
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


@final
@dataclass(frozen=True, slots=True)
class FSAPIDTOMapper(FSAPIDtoEntityMapperProtocol):

    def to_calls_dict(self, dto: ShowCallsDTO) -> dict:
        return {
            'call_uuid': str(dto.call_uuid),
            'direction': dto.direction,
        }

    def to_calls_dto(self, data: dict) -> ShowCallsDTO:
        return ShowCallsDTO(
            call_uuid=UUID(data['uuid']),
            name=data['name'],
            cid_num=data['cid_num'],
            b_cid_num=data['b_dest'],
            direction=data['direction'],
        )
