from abc import abstractmethod
from typing import Protocol

from src.application.numbers.dtos.number import NumberDTO
from src.domain.numbers.entities.numbers import Numbers


class NumbersDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: NumberDTO) -> Numbers:
        ...

    @abstractmethod
    def to_dto(self, entity: Numbers) -> NumberDTO:
        ...
