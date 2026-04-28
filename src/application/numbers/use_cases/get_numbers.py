from dataclasses import dataclass

from src.application.numbers.dtos.number import NumberDTO
from src.application.numbers.ports.mappers import NumbersDtoEntityMapperProtocol
from src.application.numbers.ports.repository import NumbersRepositoryProtocol


@dataclass
class GetNumbersUseCase:
    _number_repository: NumbersRepositoryProtocol
    _number_mapper: NumbersDtoEntityMapperProtocol

    async def __call__(self) -> list[NumberDTO]:
        number_entities = await self._number_repository.get_numbers()
        return [self._number_mapper.to_dto(number_entity) for number_entity in number_entities]
