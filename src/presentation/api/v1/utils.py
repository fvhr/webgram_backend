from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi.requests import Request

from src.application.common.exceptions import ForbiddenError
from src.application.user.ports.auth import AuthentificationProtocol
from src.application.user.service.require_role_service import RequireRoleService
from src.settings import Settings


def require_roles(roles: List[str]):
    @inject
    async def role_checker(request: Request,
                           service: FromDishka[RequireRoleService],
                           settings: FromDishka[Settings],
                           ) -> None:
        cookies = request.cookies
        token = cookies.get(settings.CONFIG.JWT_ACCESS_COOKIE_NAME, None)
        await service(roles, token)

    return role_checker


def require_authorization():
    """Создает зависимость для проверки авторизации"""

    @inject
    def authorization_checker(
            request: Request,
            service: FromDishka[AuthentificationProtocol],
            settings: FromDishka[Settings],
    ) -> None:
        cookies = request.cookies
        token = cookies.get(settings.CONFIG.JWT_ACCESS_COOKIE_NAME, None)
        user_uuid = service.get_user_uuid_by_token(token)
        if not user_uuid:
            raise ForbiddenError('Authorization required')
        return None

    return authorization_checker
