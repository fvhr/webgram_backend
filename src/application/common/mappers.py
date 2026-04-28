from dataclasses import dataclass
from typing import final
from uuid import UUID

from src.application.common.dtos.cdr import CDREveryMinute
from src.application.common.dtos.event import EventDTO
from src.application.common.dtos.fsapi import ShowCallsDTO
from src.application.common.dtos.system_resources import RAMDTO, CPUDTO, DiskDTO
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol, FSAPIDtoEntityMapperProtocol, \
    CDREveryMinuteDtoDictMapperProtocol, SystemEventsDtoDictMapperProtocol
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


@final
@dataclass(frozen=True, slots=True)
class CDREveryMinuteDTOMapper(CDREveryMinuteDtoDictMapperProtocol):
    def to_dto(self, data: dict) -> CDREveryMinute:
        return CDREveryMinute(
            hour_of_day=data['hour_of_day'],
            minute_of_hour=data['minute_of_hour'],
            call_count=data['call_count']
        )

    def to_dict(self, dto: CDREveryMinute) -> dict:
        return {
            'hour_of_day': dto.hour_of_day,
            'minute_of_hour': dto.minute_of_hour,
            'call_count': dto.call_count,
        }


@final
@dataclass(frozen=True, slots=True)
class SystemEventsDTOMapper(SystemEventsDtoDictMapperProtocol):
    def to_dict(self, ram_dto: RAMDTO, cpu_dto: CPUDTO, disk_dto: DiskDTO) -> dict:
        return {
            'ram': {
                'total_gb': ram_dto.total_gb,
                'used_gb': ram_dto.used_gb,
                'free_gb': ram_dto.free_gb,
            },
            'disk': {
                'total_gb': disk_dto.total_gb,
                'used_gb': disk_dto.used_gb,
                'free_gb': disk_dto.free_gb,
            },
            'cpu': {
                'cpu_usage_percent': cpu_dto.cpu_usage_percent,
                'cpu_free_percent': cpu_dto.cpu_free_percent,
            },
        }
