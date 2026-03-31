from dataclasses import dataclass

from src.application.common.exceptions import ForbiddenError
from src.application.user.dtos.user import LoginDTO, TokensDTO
from src.application.user.ports.auth import AuthentificationProtocol
from src.application.user.ports.repository import ViewUserRepositoryProtocol
from src.domain.services.password_hash_service import PasswordHashService


@dataclass
class LoginService:
    _authentication: AuthentificationProtocol
    _password_hash: PasswordHashService
    _user_view_repo: ViewUserRepositoryProtocol

    async def __call__(self, login_data: LoginDTO) -> TokensDTO:
        verify_data = await self._user_view_repo.get_verify_password_data(login_data.user_name)
        if not verify_data or not self._password_hash.verify_password(login_data.user_password,
                                                                      verify_data.password_hash):
            raise ForbiddenError('Incorrect username or password')
        access_token = self._authentication.get_access_token(str(verify_data.user_uuid))
        refresh_token = self._authentication.get_refresh_token(str(verify_data.user_uuid))
        return TokensDTO(access_token=access_token, refresh_token=refresh_token)
