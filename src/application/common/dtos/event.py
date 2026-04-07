from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass
class EventDTO(DTO):
    headers: dict
