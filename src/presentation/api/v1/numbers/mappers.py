from dataclasses import dataclass
from typing import final

from src.application.numbers.dtos.number import NumberDTO
from src.presentation.api.v1.numbers.schemas.responses import NumbersResponseSchema
from src.presentation.api.v1.numbers.schemas.schema import NumbersSchema


@final
@dataclass(frozen=True, slots=True)
class NumbersPresentationMapper:
    @staticmethod
    def to_response(dto: NumberDTO) -> NumbersResponseSchema:
        """Convert Application DTO to API Response model."""
        return NumbersResponseSchema(
            number_uuid=dto.number_uuid,
            number_name=dto.number_name,
            number_number=dto.number_number,
        )

    @staticmethod
    def to_dto(schema: NumbersSchema) -> NumberDTO:
        """Convert Application DTO to API Response model."""
        return NumberDTO(
            number_uuid=schema.number_uuid,
            number_name=schema.number_name,
            number_number=schema.number_number,
        )
