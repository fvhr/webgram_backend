from abc import abstractmethod
from typing import Protocol

from src.application.domain.dtos.domain import DomainDTO
from src.domain.domain.entities.domain import Domain


class DomainDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: DomainDTO) -> Domain:
        ...

    @abstractmethod
    def to_dto(self, entity: Domain) -> DomainDTO:
        ...
