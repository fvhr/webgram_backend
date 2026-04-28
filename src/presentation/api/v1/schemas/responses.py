from pydantic import BaseModel


class CdrEveryMinuteResponseSchema(BaseModel):
    hour_of_day: str
    minute_of_hour: str
    call_count: int
