from dataclasses import dataclass

from src.application.common.exceptions import ForbiddenError
from src.application.user.dtos.user import RefreshDTO
from src.application.user.ports.auth import AuthentificationProtocol


@dataclass
class RefreshService:
    _authentication: AuthentificationProtocol

    async def __call__(self, token: str) -> RefreshDTO:
        user_uuid = self._authentication.get_user_uuid_by_token(token)
        if not user_uuid:
            raise ForbiddenError('Refresh token required')
        access_token = self._authentication.get_access_token(str(user_uuid))
        return RefreshDTO(access_token=access_token)
