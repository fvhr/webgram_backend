from dataclasses import dataclass
from uuid import UUID

from src.domain.numbers.value_objects.number import NumberNumber


@dataclass
class Numbers:
    number_uuid: UUID
    number_name: str
    number_number: NumberNumber
