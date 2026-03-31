import uuid
from dataclasses import dataclass

from src.application.common.exceptions import AlreadyExistsError
from src.application.user.ports.repository import ViewUserRepositoryProtocol, RoleRepositoryProtocol, \
    UserRepositoryProtocol
from src.domain.user.entities.role import Role
from src.domain.user.entities.user import User
from src.domain.user.value_objects.role_name import RoleName
from src.domain.user.value_objects.user_name import UserName
from src.domain.user.value_objects.user_password import UserPassword
from src.settings.config import Settings


@dataclass
class CreateDefaultRoleAndUserService:
    _settings: Settings
    _user_repo: UserRepositoryProtocol
    _user_view_repo: ViewUserRepositoryProtocol
    _role_repo: RoleRepositoryProtocol

    async def __call__(self) -> None:
        role = await self._role_repo.get_role_by_role_name(self._settings.DEFAULT_ROLE)
        if not role:
            role = Role(
                role_uuid=uuid.uuid4(),
                role_name=RoleName(self._settings.DEFAULT_ROLE)
            )
            role = await self._role_repo.create_role(role)
            if not role:
                raise AlreadyExistsError(f'Failed save "{role}"')

        user = await self._user_view_repo.get_user_by_user_name(self._settings.DEFAULT_ADMIN_NAME)
        if not user:
            user = User(
                user_uuid=uuid.uuid4(),
                user_name=UserName(self._settings.DEFAULT_ADMIN_NAME),
                user_password=UserPassword(self._settings.DEFAULT_ADMIN_PASSWORD),
                role_uuid=role.role_uuid,
            )
            user_uuid = await self._user_repo.create_user(user)
            if not user_uuid:
                raise AlreadyExistsError(f'Failed save "{user}"')
