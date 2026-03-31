from dataclasses import dataclass

from src.application.common.exceptions import NotFoundError
from src.application.user.dtos.user import UpdateUserDTO, OutboundUserDTO
from src.application.user.ports.repository import UserRepositoryProtocol, ViewUserRepositoryProtocol


@dataclass
class UpdateUserUseCase:
    _user_repository: UserRepositoryProtocol
    _user_view_repo: ViewUserRepositoryProtocol

    async def __call__(self, dto: UpdateUserDTO) -> OutboundUserDTO:
        user_uuid = await self._user_repository.update_user(dto)
        if not user_uuid:
            raise NotFoundError(
                f'User with "{dto.user_uuid}" not found'
            )
        user_out_dto = await self._user_view_repo.get_user(str(user_uuid))
        if not user_out_dto:
            raise NotFoundError(
                f'User with "{dto.user_uuid}" not found'
            )
        return user_out_dto
