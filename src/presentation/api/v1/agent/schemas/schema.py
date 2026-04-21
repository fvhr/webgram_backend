from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class SetStatusAgent(BaseModel):
    agent_uuid: UUID
    agent_status: Literal['Available', 'Logged Out']
