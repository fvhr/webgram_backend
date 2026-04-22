from uuid import UUID

from pydantic import BaseModel


class QueueResponseSchema(BaseModel):
    queue_uuid: UUID
    queue_name: str
