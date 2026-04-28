from abc import abstractmethod
from typing import Protocol

from src.domain.numbers.entities.numbers import Numbers


class NumbersRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_number(self, number: Numbers) -> Numbers:
        raise NotImplementedError

    @abstractmethod
    async def delete_number(self, number_uuid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_numbers(self) -> list[Numbers]:
        raise NotImplementedError

    @abstractmethod
    async def update_number(self, number: Numbers) -> Numbers:
        raise NotImplementedError
