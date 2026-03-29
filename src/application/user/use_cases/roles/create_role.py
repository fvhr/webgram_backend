from dataclasses import dataclass

from src.application.common.exceptions import AlreadyExistsError
from src.application.user.dtos.role import RoleDTO
from src.application.user.ports.mappers import RoleDtoEntityMapperProtocol
from src.application.user.ports.repository import RoleRepositoryProtocol


@dataclass
class CreateRoleUseCase:
    _role_repository: RoleRepositoryProtocol
    _role_mapper: RoleDtoEntityMapperProtocol

    async def __call__(self, role: RoleDTO) -> RoleDTO:
        role_entity = self._role_mapper.to_entity(role)
        role_entity = await self._role_repository.create_role(role_entity)
        if role_entity:
            role_dto = self._role_mapper.to_dto(role_entity)
            return role_dto
        raise AlreadyExistsError(f'Failed save "{role_entity}"')
