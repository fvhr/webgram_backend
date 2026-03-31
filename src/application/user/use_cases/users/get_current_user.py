from dataclasses import dataclass

from src.application.common.exceptions import NotFoundError, ForbiddenError
from src.application.user.dtos.user import OutboundUserDTO
from src.application.user.ports.auth import AuthentificationProtocol
from src.application.user.ports.repository import ViewUserRepositoryProtocol


@dataclass
class GetCurrentUserUseCase:
    _user_view_repo: ViewUserRepositoryProtocol
    _authentication: AuthentificationProtocol

    async def __call__(self, token: str | None) -> OutboundUserDTO:
        user_uuid = self._authentication.get_user_uuid_by_token(token)
        if not user_uuid:
            raise ForbiddenError(f'Authentification required')

        user_out_dto = await self._user_view_repo.get_user(str(user_uuid))
        if not user_out_dto:
            raise NotFoundError(f'User with "{user_uuid}" not found')
        return user_out_dto
