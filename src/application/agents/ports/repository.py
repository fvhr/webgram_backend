from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.agents.dtos.agent import AgentDTO
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

    @abstractmethod
    async def change_status_agent(self, agent_uuid: str, new_status: str) -> Agent:
        raise NotImplementedError

    @abstractmethod
    async def get_free_agents(self) -> list[Agent]:
        raise NotImplementedError

    @abstractmethod
    async def set_user(self, agent_uuid: str, user_uuid: UUID) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_agent_uuid_by_agent_num(self, agent_num: str) -> UUID | None:
        raise NotImplementedError


class ViewAgentRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_agent(self, agent_uuid: str) -> AgentDTO | None:
        raise NotImplementedError
