from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Optional

from src.application.agents.dtos.agent import AgentAtcDTO, AgentHistoryDTO
from src.application.common.dtos.cdr import CDREveryMinute
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

    @abstractmethod
    async def get_atc_history_agent_by_day(self, agent_number: str) -> list[AgentHistoryDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_count_cdr_every_minute(self, start_date: datetime, end_date: datetime) -> list[CDREveryMinute]:
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


class RedisClientProtocol(Protocol):

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    async def delete(self, key: str) -> int:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass
