from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


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
