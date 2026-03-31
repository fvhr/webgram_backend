from dataclasses import dataclass

from src.application.user.dtos.user import OutboundUserDTO
from src.application.user.ports.repository import ViewUserRepositoryProtocol


@dataclass
class GetUsersUseCase:
    _user_view_repo: ViewUserRepositoryProtocol

    async def __call__(self) -> list[OutboundUserDTO]:
        return await self._user_view_repo.get_users()
