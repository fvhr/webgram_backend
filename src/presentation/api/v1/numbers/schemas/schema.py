from uuid import UUID

from pydantic import BaseModel


class NumbersSchema(BaseModel):
    number_uuid: UUID
    number_name: str
    number_number: str
