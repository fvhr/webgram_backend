from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from src.application.common.exceptions import ForbiddenError
from src.application.user.ports.auth import AuthentificationProtocol
from src.application.user.service.require_role_service import RequireRoleService


def require_roles(roles: List[str]):
    @inject
    async def role_checker(service: FromDishka[RequireRoleService]) -> None:
        await service(roles)

    return role_checker


def require_authorization():
    """Создает зависимость для проверки авторизации"""

    @inject
    def authorization_checker(
            service: FromDishka[AuthentificationProtocol]
    ) -> None:
        user_uuid = service.get_user_uuid_access_token()
        if not user_uuid:
            raise ForbiddenError('Authorization required')
        return None

    return authorization_checker
