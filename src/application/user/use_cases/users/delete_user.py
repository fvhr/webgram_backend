from dataclasses import dataclass

from src.application.user.ports.repository import UserRepositoryProtocol


@dataclass
class DeleteUserUseCase:
    _user_repository: UserRepositoryProtocol

    async def __call__(self, user_uuid: str) -> None:
        await self._user_repository.delete_user(user_uuid)