from abc import abstractmethod
from typing import Protocol

from src.domain.agents.entities.agent import Agent


class AgentRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_or_update_all_agents(self, agents: list[Agent]) -> list[Agent]:
        raise NotImplementedError

    @abstractmethod
    async def delete_agent(self, agent_uuid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_agents(self) -> list[Agent]:
        raise NotImplementedError
