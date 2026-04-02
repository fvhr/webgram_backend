from dataclasses import dataclass
from uuid import UUID

from src.domain.domain.value_objects.domain_name import DomainName


@dataclass
class Domain:
    domain_uuid: UUID
    domain_name: DomainName
    domain_enabled: bool
    domain_description: str | None
