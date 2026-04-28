import asyncio
import datetime
from typing import Any

import pytz


async def scheduler(use_case: Any, interval: int = 5):
    while True:
        await use_case()
        await asyncio.sleep(interval)


def convert_to_moscow_time(value: datetime.datetime | None) -> datetime.datetime | None:
    moscow_tz = pytz.timezone('Europe/Moscow')
    if not value:
        value = datetime.datetime.now(tz=moscow_tz)
    if value is not None:
        if value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)
        value = value.astimezone(moscow_tz)
        return value.replace(tzinfo=None)
    return None
