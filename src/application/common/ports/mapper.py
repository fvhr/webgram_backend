from abc import abstractmethod
from typing import Protocol

from src.application.common.dtos.event import EventDTO
from src.domain.events.entities.custom_event import CustomEvent


class EventDtoEntityMapperProtocol(Protocol):
    @abstractmethod
    def to_entity_custom(self, dto: EventDTO) -> CustomEvent:
        ...
