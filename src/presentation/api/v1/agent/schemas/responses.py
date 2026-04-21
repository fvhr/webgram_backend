from uuid import UUID

from pydantic import BaseModel


class AgentResponseSchema(BaseModel):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None
    agent_password: str | None
    domain_uuid: UUID
    agent_status: str
