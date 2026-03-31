from abc import abstractmethod
from typing import Protocol

from src.application.user.dtos.role import RoleDTO
from src.application.user.dtos.user import InboundUserDTO, UpdateUserDTO
from src.domain.user.entities.role import Role
from src.domain.user.entities.user import User


class RoleDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: RoleDTO) -> Role:
        ...

    @abstractmethod
    def to_dto(self, entity: Role) -> RoleDTO:
        ...


class UserDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: InboundUserDTO) -> User:
        ...