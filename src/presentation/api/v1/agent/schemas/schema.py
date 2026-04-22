from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class SetStatusAgent(BaseModel):
    agent_uuid: UUID
    agent_status: Literal['Available', 'Logged Out']


class SetQueuesAgent(BaseModel):
    agent_uuid: UUID
    queue_uuids: list[UUID]
