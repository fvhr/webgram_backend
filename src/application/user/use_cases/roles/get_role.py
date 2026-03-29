from dataclasses import dataclass

from src.application.common.exceptions import NotFoundError
from src.application.user.dtos.role import RoleDTO
from src.application.user.ports.mappers import RoleDtoEntityMapperProtocol
from src.application.user.ports.repository import RoleRepositoryProtocol


@dataclass
class GetRoleUseCase:
    _role_repository: RoleRepositoryProtocol
    _role_mapper: RoleDtoEntityMapperProtocol

    async def __call__(self, role_uuid: str) -> RoleDTO:
        role_entity = await self._role_repository.get_role(role_uuid)
        if role_entity:
            role_dto = self._role_mapper.to_dto(role_entity)
            return role_dto
        raise NotFoundError(f'Role with "{role_uuid}" not found')
