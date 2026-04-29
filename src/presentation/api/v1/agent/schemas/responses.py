import datetime
from uuid import UUID

from pydantic import BaseModel

from src.presentation.api.v1.queue.schemas.responses import QueueResponseSchema
from src.presentation.api.v1.schemas.responses import DomainResponseSchema


class AgentFreeResponseSchema(BaseModel):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None


class AgentResponseSchema(BaseModel):
    agent_uuid: UUID
    agent_name: str
    agent_number: str | None
    agent_password: str | None
    agent_status: str
    domain: DomainResponseSchema
    queues: list[QueueResponseSchema]


class AgentHistoryResponseSchema(BaseModel):
    start_stamp: datetime.datetime
    duration: str
    direction: str
    caller_id_number: str
    destination_number: str
