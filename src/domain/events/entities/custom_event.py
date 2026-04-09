from dataclasses import dataclass

from src.domain.events.entities.base_event import BaseEvent


@dataclass
class CustomEvent(BaseEvent):
    event_action: str | None
    event_agent_uuid: str | None
    event_agent_status: str | None
