from abc import abstractmethod
from typing import Protocol

from src.application.agents.dtos.agent import AgentAtcDTO
from src.application.extensions.dtos.extension import ExtensionAtcDTO
from src.domain.domain.entities.domain import Domain


class AtcGatewayProtocol(Protocol):
    @abstractmethod
    async def get_atc_domains(self) -> list[Domain]:
        raise NotImplementedError

    @abstractmethod
    async def get_atc_agents(self) -> list[AgentAtcDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_atc_extensions(self) -> list[ExtensionAtcDTO]:
        raise NotImplementedError
