from dataclasses import dataclass

from src.application.common.exceptions import NotFoundError
from src.application.user.dtos.user import OutboundUserDTO
from src.application.user.ports.repository import ViewUserRepositoryProtocol


@dataclass
class GetUserUseCase:
    _user_view_repo: ViewUserRepositoryProtocol

    async def __call__(self, user_uuid: str) -> OutboundUserDTO:
        user_out_dto = await self._user_view_repo.get_user(user_uuid)
        if not user_out_dto:
            raise NotFoundError(
                f'User with "{user_uuid}" not found'
            )
        return user_out_dto
