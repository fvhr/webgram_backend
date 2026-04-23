from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass
class ShowCallsDTO(DTO):
    call_uuid: UUID
    name: str
    cid_num: str
    b_cid_num: str
    direction: str
