from dataclasses import dataclass
from typing import final

from genesis import ESLEvent

from src.application.common.dtos.event import EventDTO


@final
@dataclass(frozen=True, slots=True)
class EventMapper:
    @staticmethod
    def to_dto(event: ESLEvent) -> EventDTO:
        return EventDTO(
            headers=dict(event),
        )
