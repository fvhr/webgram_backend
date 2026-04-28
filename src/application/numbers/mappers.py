from dataclasses import dataclass
from typing import final

from src.application.numbers.dtos.number import NumberDTO
from src.application.numbers.ports.mappers import NumbersDtoEntityMapperProtocol
from src.domain.numbers.entities.numbers import Numbers
from src.domain.numbers.value_objects.number import NumberNumber


@final
@dataclass(frozen=True, slots=True)
class NumbersDTOMapper(NumbersDtoEntityMapperProtocol):

    def to_entity(self, dto: NumberDTO) -> Numbers:
        return Numbers(
            number_uuid=dto.number_uuid,
            number_name=dto.number_name,
            number_number=NumberNumber(dto.number_number),
        )

    def to_dto(self, entity: Numbers) -> NumberDTO:
        return NumberDTO(
            number_uuid=entity.number_uuid,
            number_name=entity.number_name,
            number_number=entity.number_number.value,
        )
