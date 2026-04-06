from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class QueueAtcDTO(DTO):
    queue_uuid: UUID
    queue_name: str
    queue_number: str
    domain_uuid: UUID
