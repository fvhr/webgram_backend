from dataclasses import dataclass

from src.application.common.exceptions import NotFoundError
from src.application.user.dtos.user import UpdatePasswordDTO, OutboundUserDTO
from src.application.user.ports.repository import UserRepositoryProtocol, ViewUserRepositoryProtocol
from src.domain.user.value_objects.user_password import UserPassword


@dataclass
class ChangePasswordUseCase:
    _user_repo: UserRepositoryProtocol
    _user_view_repo: ViewUserRepositoryProtocol

    async def __call__(self, user_uuid: str, new_password: UpdatePasswordDTO) -> OutboundUserDTO:
        validate_password = UserPassword(new_password.password)
        user_uuid = await self._user_repo.change_password(user_uuid, validate_password.value)
        if user_uuid:
            return await self._user_view_repo.get_user(str(user_uuid))
        raise NotFoundError(
            f'User with "{user_uuid}" not found'
        )
