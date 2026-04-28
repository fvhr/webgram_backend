from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.application.common.dtos.cdr import CDREveryMinute


@final
@dataclass(frozen=True, slots=True)
class CDREveryMinuteGatewayDBMapper:
    @staticmethod
    def to_dto(model: Row) -> CDREveryMinute:
        return CDREveryMinute(
            hour_of_day=model.hour_of_day,
            minute_of_hour=model.minute_of_hour,
            call_count=model.call_count,
        )
