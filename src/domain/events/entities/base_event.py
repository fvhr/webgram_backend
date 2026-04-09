from dataclasses import dataclass

from enum import StrEnum


class EventTypes(StrEnum):
    HEARTBEAT = 'HEARTBEAT'
    CUSTOM = 'CUSTOM'


@dataclass
class BaseEvent:
    event_name: str
