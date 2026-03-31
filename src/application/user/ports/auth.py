from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class AuthentificationProtocol(Protocol):
    @abstractmethod
    def get_user_uuid_access_token(self) -> UUID | None:
        ...

    @abstractmethod
    def get_access_token(self, user_uuid: str) -> str:
        ...

    @abstractmethod
    def get_refresh_token(self, user_uuid: str) -> str:
        ...

    @abstractmethod
    def get_user_uuid_refresh_token(self) -> UUID | None:
        ...
