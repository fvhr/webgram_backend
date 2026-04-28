from dataclasses import dataclass

from src.application.common.exceptions import AlreadyExistsError
from src.application.numbers.dtos.number import NumberDTO
from src.application.numbers.ports.mappers import NumbersDtoEntityMapperProtocol
from src.application.numbers.ports.repository import NumbersRepositoryProtocol


@dataclass
class CreateNumberUseCase:
    _number_repository: NumbersRepositoryProtocol
    _number_mapper: NumbersDtoEntityMapperProtocol

    async def __call__(self, dto: NumberDTO) -> NumberDTO | None:
        number_entity = self._number_mapper.to_entity(dto)
        number_entity = await self._number_repository.create_number(number_entity)
        if number_entity:
            number_dto = self._number_mapper.to_dto(number_entity)
            return number_dto
        raise AlreadyExistsError(
            f'Entity with number_uuid "{dto.number_uuid}" already exists'
        )
