from abc import abstractmethod
from typing import Protocol

from src.application.user.dtos.user import OutboundUserDTO
from src.domain.user.entities.role import Role
from src.domain.user.entities.user import User


class RoleRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_role(self, role_uuid: str) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def get_roles(self) -> list[Role]:
        raise NotImplementedError

    @abstractmethod
    async def create_role(self, role: Role) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def update_role(self, role: Role) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_role(self, role_uuid: str) -> None:
        raise NotImplementedError


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_user(self, user: User) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_uuid: str) -> None:
        raise NotImplementedError


class ViewUserRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_user(self, user_uuid: str) -> OutboundUserDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self) -> list[OutboundUserDTO]:
        raise NotImplementedError
