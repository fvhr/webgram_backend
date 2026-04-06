from dataclasses import dataclass
from uuid import UUID

from src.domain.agents.value_objects.agent_number import AgentNumber


@dataclass
class Agent:
    agent_uuid: UUID
    agent_name: str
    agent_number: AgentNumber
    agent_password: str | None
    domain_uuid: UUID
    user_uuid: UUID | None = None
    agent_status: str = 'Logged Out'
