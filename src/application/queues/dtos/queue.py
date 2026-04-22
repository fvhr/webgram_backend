from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO
from src.application.domain.dtos.domain import DomainDTO


@dataclass(frozen=True)
class QueueAtcDTO(DTO):
    queue_uuid: UUID
    queue_name: str
    queue_number: str
    domain_uuid: UUID


@dataclass(frozen=True)
class QueueDTO(DTO):
    queue_uuid: UUID
    queue_name: str


@dataclass(frozen=True)
class ViewQueueDTO(DTO):
    queue_uuid: UUID
    queue_number: str
    domain: DomainDTO
