from uuid import UUID

from pydantic import BaseModel


class CdrEveryMinuteResponseSchema(BaseModel):
    hour_of_day: str
    minute_of_hour: str
    call_count: int

class DomainResponseSchema(BaseModel):
    domain_uuid: UUID
    domain_name: str