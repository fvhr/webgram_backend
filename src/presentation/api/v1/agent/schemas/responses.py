from uuid import UUID

from pydantic import BaseModel

from src.presentation.api.v1.queue.schemas.responses import QueueResponseSchema


class AgentFreeResponseSchema(BaseModel):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None


class AgentResponseSchema(BaseModel):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None
    agent_password: str | None
    domain_uuid: UUID
    agent_status: str
    queues: list[QueueResponseSchema]
