from dataclasses import dataclass

from src.application.user.dtos.role import RoleDTO
from src.application.user.ports.mappers import RoleDtoEntityMapperProtocol
from src.application.user.ports.repository import RoleRepositoryProtocol


@dataclass
class GetRolesUseCase:
    _role_repository: RoleRepositoryProtocol
    _role_mapper: RoleDtoEntityMapperProtocol

    async def __call__(self) -> list[RoleDTO]:
        roles = await self._role_repository.get_roles()
        return [self._role_mapper.to_dto(role) for role in roles]
