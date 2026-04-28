from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass
class CDREveryMinute(DTO):
   hour_of_day: str
   minute_of_hour: str
   call_count: int
