import datetime
import json
from dataclasses import dataclass
from json import JSONDecodeError

from src.application.common.dtos.cdr import CDREveryMinute
from src.application.common.ports.external import RedisClientProtocol, AtcGatewayProtocol
from src.application.common.ports.mapper import CDREveryMinuteDtoDictMapperProtocol
from src.utils import convert_to_moscow_time


@dataclass
class GetCountCDREveryMinute:
    _redis: RedisClientProtocol
    _mapper: CDREveryMinuteDtoDictMapperProtocol
    _atc_gateway: AtcGatewayProtocol

    async def __call__(self, year: int, month: int, day: int) -> list[CDREveryMinute]:
        start_date = datetime.datetime(year, month, day, 0, 0)
        end_date = start_date + datetime.timedelta(days=1)
        key = f"cdr_count_every_day_{start_date.year}_{start_date.month}_{start_date.day}"

        rows = await self._get_from_redis(key)
        if rows:
            return [self._mapper.to_dto(row) for row in rows]
        else:
            rows = await self._atc_gateway.get_count_cdr_every_minute(start_date, end_date)
            now_date = convert_to_moscow_time(None)
            is_today = (
                    now_date.year == start_date.year
                    and now_date.month == start_date.month
                    and now_date.day == start_date.day
            )
            if is_today:
                rows_for_redis = [self._mapper.to_dict(dto) for dto in rows]
                await self._set_in_redis(key, rows_for_redis)
            return rows

    async def _get_from_redis(self, key: str) -> dict | None:
        if await self._redis.exists(key):
            rows = await self._redis.get(key)
            try:
                return json.loads(rows)
            except JSONDecodeError:
                return None
        return None

    async def _set_in_redis(self, key: str, data: list) -> None:
        value = json.dumps(data)
        await self._redis.set(key, value, expire=86400)
