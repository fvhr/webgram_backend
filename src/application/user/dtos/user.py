from dataclasses import dataclass
from typing import Optional
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
class UpdateUserDTO(DTO):
    user_uuid: UUID
    user_name: str
    role_uuid: UUID


@dataclass(frozen=True)
class UpdatePasswordDTO(DTO):
    password: str


@dataclass(frozen=True)
class OutboundUserDTO(DTO):
    user_uuid: UUID
    user_name: str
    role: RoleDTO


@dataclass(frozen=True)
class LoginDTO(DTO):
    user_name: str
    user_password: str


@dataclass(frozen=True)
class TokensDTO:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class VerifyPasswordDTO(DTO):
    user_uuid: UUID
    password_hash: str


@dataclass(frozen=True)
class RefreshDTO:
    access_token: str
