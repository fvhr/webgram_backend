from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class RoleDTO(DTO):
    role_uuid: UUID
    role_name: str
