from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class ExtensionAtcDTO(DTO):
    extension_uuid: UUID
    extension_number: str
    extension_password: str | None
    caller_id_name: str | None
    caller_id_number: str | None
    domain_uuid: UUID
