from abc import abstractmethod
from typing import Protocol

from src.domain.extensions.entities.extension import Extension


class ExtensionDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: ExtensionAtcDTO) -> Extension:
        ...