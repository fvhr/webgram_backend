from dataclasses import dataclass

from src.application.common.exceptions import ForbiddenError
from src.application.user.use_cases.users.get_current_user import GetCurrentUserUseCase


@dataclass
class RequireRoleService:
    _get_current_user_use_case: GetCurrentUserUseCase

    async def __call__(self, required_roles: list, token: str | None) -> None:
        """Проверяет, имеет ли пользователь необходимые роли"""
        user_out_dto = await self._get_current_user_use_case(token)

        if user_out_dto.role.role_name not in required_roles:
            raise ForbiddenError("Insufficient permissions")
