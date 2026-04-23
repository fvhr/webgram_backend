from abc import abstractmethod
from typing import Protocol

from src.application.common.dtos.event import EventDTO
from src.application.common.dtos.fsapi import ShowCallsDTO
from src.domain.events.entities.custom_event import CustomEvent


class EventDtoEntityMapperProtocol(Protocol):
    @abstractmethod
    def to_entity_custom(self, dto: EventDTO) -> CustomEvent:
        ...


class FSAPIDtoEntityMapperProtocol(Protocol):
    @abstractmethod
    def to_calls_dto(self, data: dict) -> ShowCallsDTO:
        ...

    @abstractmethod
    def to_calls_dict(self, dto: ShowCallsDTO) -> dict:
        ...
