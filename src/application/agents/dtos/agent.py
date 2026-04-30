import datetime
from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO
from src.application.domain.dtos.domain import DomainDTO
from src.application.queues.dtos.queue import QueueDTO


@dataclass(frozen=True)
class AgentAtcDTO(DTO):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None
    agent_password: str
    domain_uuid: UUID


@dataclass(frozen=True)
class AgentDTO(DTO):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None
    agent_password: str | None
    domain_uuid: UUID
    agent_status: str
    domain: DomainDTO
    queues: list[QueueDTO]


@dataclass(frozen=True)
class AgentFreeDTO(DTO):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None


@dataclass(frozen=True)
class AgentHistoryDTO:
    start_stamp: datetime.datetime
    duration: str
    direction: str
    caller_id_number: str
    destination_number: str