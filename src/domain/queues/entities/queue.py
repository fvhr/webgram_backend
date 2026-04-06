from dataclasses import dataclass
from uuid import UUID


@dataclass
class Queue:
    queue_uuid: UUID
    queue_name: str
    queue_number: str
    domain_uuid: UUID
