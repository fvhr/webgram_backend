from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO
from src.application.user.dtos.role import RoleDTO


@dataclass(frozen=True)
class InboundUserDTO(DTO):
    user_uuid: UUID
    user_name: str
    user_password: str
    role_uuid: UUID


@dataclass(frozen=True)
class OutboundUserDTO(DTO):
    user_uuid: UUID
    user_name: str
    role: RoleDTO
