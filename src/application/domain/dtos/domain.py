from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class DomainDTO(DTO):
    domain_uuid: UUID
    domain_name: str
    domain_enabled: bool
    domain_description: str | None
