from abc import abstractmethod
from typing import Protocol

from src.application.agents.dtos.agent import AgentAtcDTO
from src.domain.agents.entities.agent import Agent


class AgentDtoEntityMapperProtocol(Protocol):

    @abstractmethod
    def to_entity(self, dto: AgentAtcDTO) -> Agent:
        ...

    @abstractmethod
    def to_dict(self, entity: Agent) -> dict:
        ...