from dataclasses import dataclass

from src.application.user.ports.repository import RoleRepositoryProtocol


@dataclass
class DeleteRoleUseCase:
    _role_repository: RoleRepositoryProtocol

    async def __call__(self, role_uuid: str) -> None:
        await self._role_repository.delete_role(role_uuid)
