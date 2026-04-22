from dataclasses import dataclass
from uuid import UUID


@dataclass
class Tier:
    tier_uuid: UUID
    agent_uuid: UUID
    queue_uuid: UUID