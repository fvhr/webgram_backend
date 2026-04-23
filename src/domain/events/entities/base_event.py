from dataclasses import dataclass

from enum import StrEnum


class EventTypes(StrEnum):
    HEARTBEAT = 'HEARTBEAT'
    CUSTOM = 'CUSTOM'
    CHANNEL_CREATE = 'CHANNEL_CREATE'
    CHANNEL_DESTROY = 'CHANNEL_DESTROY'
    CHANNEL_ANSWER = 'CHANNEL_ANSWER'


@dataclass
class BaseEvent:
    event_name: str
