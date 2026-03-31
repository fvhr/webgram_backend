from dataclasses import dataclass, asdict
from typing import final

from src.application.user.dtos.role import RoleDTO
from src.application.user.dtos.user import InboundUserDTO, UpdateUserDTO
from src.application.user.ports.mappers import RoleDtoEntityMapperProtocol, UserDtoEntityMapperProtocol
from src.domain.user.entities.role import Role
from src.domain.user.entities.user import User
from src.domain.user.value_objects.role_name import RoleName
from src.domain.user.value_objects.user_name import UserName
from src.domain.user.value_objects.user_password import UserPassword


@final
@dataclass(frozen=True, slots=True)
class RoleDTOMapper(RoleDtoEntityMapperProtocol):

    def to_entity(self, dto: RoleDTO) -> Role:
        return Role(
            role_uuid=dto.role_uuid,
            role_name=RoleName(dto.role_name),
        )

    def to_dto(self, entity: Role) -> RoleDTO:
        return RoleDTO(
            role_uuid=entity.role_uuid,
            role_name=entity.role_name.value,
        )


@final
@dataclass(frozen=True, slots=True)
class UserDTOMapper(UserDtoEntityMapperProtocol):

    def to_entity(self, dto: InboundUserDTO) -> User:
        return User(
            user_uuid=dto.user_uuid,
            user_name=UserName(dto.user_name),
            user_password=UserPassword(dto.user_password),
            role_uuid=dto.role_uuid,
        )
