from dataclasses import dataclass
from typing import final

from src.domain.numbers.entities.numbers import Numbers
from src.domain.numbers.value_objects.number import NumberNumber
from src.infrastructure.db.models import NumberModel


@final
@dataclass(frozen=True, slots=True)
class NumberDBMapper:

    @staticmethod
    def to_entity(model: NumberModel) -> Numbers:
        return Numbers(
            number_uuid=model.number_uuid,
            number_name=model.number_name,
            number_number=NumberNumber(value=model.number_number)
        )

    @staticmethod
    def to_model(entity: Numbers) -> NumberModel:
        return NumberModel(
            number_uuid=entity.number_uuid,
            number_name=entity.number_name,
            number_number=entity.number_number.value,
        )

    @staticmethod
    def update_model_from_entity(model: NumberModel, entity: Numbers) -> None:
        model.number_uuid = entity.number_uuid
        model.number_name = entity.number_name
        model.number_number = entity.number_number.value
