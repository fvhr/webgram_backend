from dataclasses import dataclass

from src.application.numbers.ports.repository import NumbersRepositoryProtocol


@dataclass
class DeleteNumberUseCase:
    _number_repository: NumbersRepositoryProtocol

    async def __call__(self, number_uuid: str) -> None:
        await self._number_repository.delete_number(number_uuid)
