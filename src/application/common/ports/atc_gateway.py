from abc import abstractmethod
from typing import Protocol

from src.domain.domain.entities.domain import Domain


class AtcGatewayProtocol(Protocol):
    @abstractmethod
    async def get_atc_domains(self) -> list[Domain]:
        raise NotImplementedError
