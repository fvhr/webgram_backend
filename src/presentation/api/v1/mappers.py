from dataclasses import dataclass
from typing import final

from src.application.common.dtos.cdr import CDREveryMinute
from src.presentation.api.v1.schemas.responses import CdrEveryMinuteResponseSchema


@final
@dataclass(frozen=True, slots=True)
class CommonPresentationMapper:
    @staticmethod
    def to_cdr_count_every_minute_response(dto: CDREveryMinute) -> CdrEveryMinuteResponseSchema:
        """Convert Application DTO to API Response model."""
        return CdrEveryMinuteResponseSchema(
            hour_of_day=dto.hour_of_day,
            minute_of_hour=dto.minute_of_hour,
            call_count=dto.call_count,

        )
