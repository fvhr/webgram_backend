from abc import abstractmethod
from typing import Protocol

from src.domain.extensions.entities.extension import Extension


class ExtensionRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_or_update_extension(self, extension: Extension) -> Extension:
        raise NotImplementedError

    @abstractmethod
    async def delete_extension(self, extension_uuid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_extensions(self) -> list[Extension]:
        raise NotImplementedError
