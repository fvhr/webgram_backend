from dataclasses import dataclass

from redis import asyncio as aioredis
from typing import Optional

from src.application.common.ports.external import RedisClientProtocol


@dataclass
class AioredisClient(RedisClientProtocol):
    _redis: aioredis.Redis

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        if expire:
            return bool(await self._redis.set(key, value, ex=expire))
        return bool(await self._redis.set(key, value))

    async def delete(self, key: str) -> int:
        return await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._redis.exists(key))
