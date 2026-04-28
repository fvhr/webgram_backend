from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class NumberDTO(DTO):
    number_uuid: UUID
    number_name: str
    number_number: str