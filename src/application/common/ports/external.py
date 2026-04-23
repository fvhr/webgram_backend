from abc import abstractmethod
from typing import Protocol

from src.application.agents.dtos.agent import AgentAtcDTO
from src.application.common.dtos.fsapi import ShowCallsDTO
from src.application.extensions.dtos.extension import ExtensionAtcDTO
from src.application.queues.dtos.queue import QueueAtcDTO
from src.domain.domain.entities.domain import Domain
from src.domain.enums import WebsocketMessageTypes


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

    @abstractmethod
    async def get_atc_queues(self) -> list[QueueAtcDTO]:
        raise NotImplementedError


class WebSocketManagerProtocol(Protocol):
    @abstractmethod
    async def broadcast_message(self, type_message: WebsocketMessageTypes, data: dict) -> None:
        raise NotImplementedError


class FreeswitchAPIProtocol(Protocol):
    @abstractmethod
    async def send_command(self, command: str, params: str) -> bool:
        ...

    @abstractmethod
    async def get_calls_json(self) -> list[ShowCallsDTO]:
        ...
