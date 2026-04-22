from abc import abstractmethod
from typing import Protocol

from src.application.tiers.dtos.tier import ViewTierDTO
from src.domain.tiers.entities.tier import Tier


class TierRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_tier(self, tier: Tier) -> Tier:
        raise NotImplementedError

    @abstractmethod
    async def delete_tier(self, agent_uuid: str, queue_uuid: str) -> None:
        raise NotImplementedError


class ViewTierRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_agent_tiers(self, agent_uuid: str) -> list[ViewTierDTO]:
        raise NotImplementedError
