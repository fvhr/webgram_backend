from uuid import UUID

from pydantic import BaseModel


class NumbersResponseSchema(BaseModel):
    number_uuid: UUID
    number_name: str
    number_number: str
